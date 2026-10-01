# smalilog/lms/mcp_client.py
"""Cliente MCP para smali-lsp (JSONL y LSP framing, con timeout)."""
from __future__ import annotations

import asyncio
import json
import sys
from typing import Any

DEFAULT_TIMEOUT = 30.0  # segundos


class McpError(RuntimeError):
    """Error devuelto por el servidor MCP o por el framing."""


class SmaliMcpClient:
    def __init__(
        self,
        cmd: str,
        args: list[str] | None = None,
        *,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self.cmd = cmd
        self.args = args or []
        self.timeout = timeout
        self.proc: asyncio.subprocess.Process | None = None
        self._id = 0
        self._pending: dict[int, asyncio.Future] = {}
        self._reader: asyncio.Task | None = None
        self._stderr_task: asyncio.Task | None = None
        self._framing: str = "jsonl"  # "jsonl" | "lsp"
        self._started = False

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, *exc):
        await self.stop()

    # ---------------- ciclo de vida ----------------

    async def start(self) -> None:
        if self._started:
            return
        try:
            self.proc = await asyncio.create_subprocess_exec(
                self.cmd, *self.args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                f"No se encontró '{self.cmd}'. ¿Está en PATH? "
                f"En Termux: chmod +x $PREFIX/bin/{self.cmd}"
            ) from exc

        self._reader = asyncio.create_task(self._read_loop(), name="mcp-reader")
        self._stderr_task = asyncio.create_task(self._drain_stderr(), name="mcp-stderr")

        try:
            await self._request("initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "smalilog", "version": "0.2.0"},
            })
        except Exception:
            await self._dump_diagnostics()
            await self.stop()
            raise
        await self._notify("notifications/initialized", {})
        self._started = True

    async def stop(self) -> None:
        self._started = False
        for t in (self._reader, self._stderr_task):
            if t and not t.done():
                t.cancel()
        # fallar todas las requests pendientes
        for fut in self._pending.values():
            if not fut.done():
                fut.set_exception(McpError("cliente detenido"))
        self._pending.clear()
        if self.proc and self.proc.returncode is None:
            self.proc.terminate()
            try:
                await asyncio.wait_for(self.proc.wait(), timeout=2)
            except asyncio.TimeoutError:
                self.proc.kill()
                await self.proc.wait()

    async def _dump_diagnostics(self) -> None:
        if self.proc and self.proc.returncode is None:
            try:
                await asyncio.wait_for(self.proc.wait(), timeout=2)
            except asyncio.TimeoutError:
                self.proc.kill()
                await self.proc.wait()
        code = self.proc.returncode if self.proc else None
        sys.stderr.write(
            f"\n[smalilog] '{self.cmd} {' '.join(self.args)}' "
            f"salió con código {code}\n"
        )
        sys.stderr.write("[smalilog] Prueba a mano:\n")
        sys.stderr.write(
            f"  echo '{{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"initialize\","
            f"\"params\":{{}}}}' | {self.cmd} {' '.join(self.args)}\n"
        )

    async def _drain_stderr(self) -> None:
        assert self.proc and self.proc.stderr
        while True:
            line = await self.proc.stderr.readline()
            if not line:
                break
            sys.stderr.write("[smali-lsp] " + line.decode(errors="replace"))

    # ---------------- lectura ----------------

    async def _read_loop(self) -> None:
        assert self.proc and self.proc.stdout
        reader = self.proc.stdout
        try:
            while True:
                line = await reader.readline()
                if not line:
                    break
                s = line.strip()
                if not s:
                    continue

                # JSONL
                if s.startswith(b"{"):
                    self._framing = self._framing or "jsonl"
                    try:
                        self._handle(json.loads(s))
                    except json.JSONDecodeError:
                        continue
                    continue

                # LSP: Content-Length: N
                if s.lower().startswith(b"content-length"):
                    self._framing = "lsp"
                    try:
                        length = int(s.split(b":", 1)[1].strip())
                    except (IndexError, ValueError):
                        continue
                    # consumir headers hasta línea vacía
                    while True:
                        h = await reader.readline()
                        if not h or h in (b"\r\n", b"\n"):
                            break
                    body = await reader.readexactly(length)
                    try:
                        self._handle(json.loads(body))
                    except json.JSONDecodeError:
                        continue
                    continue
                # header desconocido → ignorar
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001
            sys.stderr.write(f"[smalilog] reader loop: {exc}\n")

    def _handle(self, msg: dict) -> None:
        rid = msg.get("id")
        if rid is None:
            return
        fut = self._pending.pop(rid, None)
        if fut is None or fut.done():
            return
        if "error" in msg:
            fut.set_exception(McpError(str(msg["error"])))
        else:
            fut.set_result(msg.get("result"))

    # ---------------- escritura ----------------

    async def _request(self, method: str, params: dict) -> Any:
        if not self.proc or not self.proc.stdin:
            raise McpError("cliente no iniciado")
        self._id += 1
        rid = self._id
        fut: asyncio.Future = asyncio.get_running_loop().create_future()
        self._pending[rid] = fut
        await self._write(json.dumps({
            "jsonrpc": "2.0", "id": rid, "method": method, "params": params,
        }))
        try:
            return await asyncio.wait_for(fut, timeout=self.timeout)
        except asyncio.TimeoutError as exc:
            self._pending.pop(rid, None)
            raise McpError(
                f"timeout ({self.timeout}s) esperando respuesta de {method}"
            ) from exc

    async def _notify(self, method: str, params: dict) -> None:
        await self._write(json.dumps({
            "jsonrpc": "2.0", "method": method, "params": params,
        }))

    async def _write(self, body: str) -> None:
        if not self.proc or not self.proc.stdin:
            raise McpError("cliente no iniciado")
        data = body.encode("utf-8")
        if self._framing == "lsp":
            header = f"Content-Length: {len(data)}\r\n\r\n".encode("ascii")
            self.proc.stdin.write(header + data)
        else:
            self.proc.stdin.write(data + b"\n")
        await self.proc.stdin.drain()

    # ---------------- API de alto nivel ----------------

    async def call_tool(self, name: str, args: dict) -> Any:
        res = await self._request("tools/call", {"name": name, "arguments": args})
        if isinstance(res, dict) and "content" in res:
            out = []
            for c in res.get("content", []):
                if c.get("type") == "text":
                    try:
                        out.append(json.loads(c["text"]))
                    except json.JSONDecodeError:
                        out.append(c["text"])
            if not out:
                return None
            return out[0] if len(out) == 1 else out
        return res


   # ---------------- atajos opcionales ----------------
# Argumentos verificados contra tools/list del server:
#   smali_index               -> {directory}
#   smali_search_symbols      -> {pattern}          (sin limit)
#   smali_find_definition     -> {symbol}
#   smali_get_stats           -> {}
#   smali_search_strings      -> {query, max_results}
#   smali_call_graph          -> {class_name, method_name, descriptor?, direction?}
#   smali_xref_summary        -> {class_name}
#   smali_type_hierarchy      -> {class_name, direction?}
#   smali_find_references     -> {uri, line, character}
#   smali_hover               -> {uri, line, character}
#   smali_diagnostics         -> {uri, content}
#   smali_document_symbols    -> {uri}

    async def index(self, directory: str) -> Any:
        return await self.call_tool("smali_index", {"directory": directory})

    async def search_symbols(self, pattern: str) -> Any:
        # OJO: el server no acepta `limit`; devuelve hasta 100.
        return await self.call_tool("smali_search_symbols", {"pattern": pattern})

    async def find_definition(self, symbol: str) -> Any:
        return await self.call_tool("smali_find_definition", {"symbol": symbol})

    async def get_stats(self) -> Any:
        return await self.call_tool("smali_get_stats", {})

    async def xref_summary(self, class_name: str) -> Any:
        return await self.call_tool("smali_xref_summary", {"class_name": class_name})

    async def search_strings(self, query: str, max_results: int = 100) -> Any:
        return await self.call_tool(
            "smali_search_strings", {"query": query, "max_results": max_results}
        )   

