#!/usr/bin/env python3
"""
Servidor TCP/HTTP ligero para recepción y registro de logs en formato JSON.

Acepta objetos sueltos y lotes (listas de objetos), que es lo que envía
el cliente nativo al agrupar logs.
"""

from __future__ import annotations

import argparse
import json
import logging
import socket
import threading
from logging.handlers import RotatingFileHandler
from typing import Optional


class LogServer:
    """Servidor TCP/HTTP ligero para recepción y registro de logs en formato JSON."""

    _DEFAULT_MAX_HEADERS = 16 * 1024
    _DEFAULT_MAX_BODY = 1024 * 1024
    _MAX_BATCH = 100
    _CLIENT_TIMEOUT = 10.0
    _ALLOWED_LEVELS = frozenset({"ERROR", "WARNING", "INFO", "DEBUG"})

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 9999,
        log_file: str = "smalilog.log",
        log_level: int = logging.INFO,
        max_headers: int = _DEFAULT_MAX_HEADERS,
        max_body: int = _DEFAULT_MAX_BODY,
    ) -> None:
        self.host = host
        self.port = port
        self.log_file = log_file
        self.max_headers = max_headers
        self.max_body = max_body
        self.is_running = False
        self._server_socket: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None
        self._stop_lock = threading.Lock()

        self.logger = logging.getLogger("smalilog.LogServer")
        self.logger.setLevel(log_level)
        self.logger.propagate = False
        if not self.logger.handlers:
            handler = RotatingFileHandler(
                log_file,
                maxBytes=5 * 1024 * 1024,
                backupCount=3,
                encoding="utf-8",
            )
            handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            )
            self.logger.addHandler(handler)

    # ---------------- HTTP helpers ---------------- #
    def _send_response(self, conn: socket.socket, status: str, body: bytes = b"") -> None:
        response = (
            f"HTTP/1.1 {status}\r\n"
            "Content-Type: application/json; charset=utf-8\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("ascii") + body
        conn.sendall(response)

    def _read_request(self, conn: socket.socket) -> bytes:
        data = b""
        while b"\r\n\r\n" not in data:
            chunk = conn.recv(4096)
            if not chunk:
                raise ValueError("Conexión cerrada")
            data += chunk
            if len(data) > self.max_headers:
                raise ValueError("Cabeceras HTTP demasiado grandes")

        headers, body = data.split(b"\r\n\r\n", 1)
        lines = headers.decode("latin-1").split("\r\n")
        if not lines or not lines[0]:
            raise ValueError("Petición HTTP vacía")

        request_line = lines[0].split()
        if len(request_line) != 3:
            raise ValueError("Línea HTTP inválida")

        method, path, version = request_line
        if method != "POST":
            raise ValueError("Método no permitido")
        if path != "/log":
            raise ValueError("Ruta no permitida")
        if version not in ("HTTP/1.0", "HTTP/1.1"):
            raise ValueError("Versión HTTP no soportada")

        content_length: Optional[int] = None
        for line in lines[1:]:
            if ":" not in line:
                continue
            name, value = line.split(":", 1)
            if name.strip().lower() == "content-length":
                try:
                    content_length = int(value.strip())
                except ValueError:
                    raise ValueError("Content-Length inválido")
                break

        if content_length is None:
            raise ValueError("Falta Content-Length")
        if content_length < 0:
            raise ValueError("Content-Length negativo")
        if content_length > self.max_body:
            raise ValueError("Cuerpo demasiado grande")

        while len(body) < content_length:
            chunk = conn.recv(4096)
            if not chunk:
                raise ValueError("Cuerpo HTTP incompleto")
            body += chunk

        return body[:content_length]

    # ---------------- Registro de entradas ---------------- #
    @staticmethod
    def _sanitize(text: str) -> str:
        """Neutraliza saltos de línea para evitar log forging."""
        return text.replace("\r", "\\r").replace("\n", "\\n")

    def _normalize_level(self, raw: object) -> str:
        level = str(raw or "INFO").strip().upper()
        return level if level in self._ALLOWED_LEVELS else "INFO"

    def _write_entry(self, level: str, entry: str) -> None:
        write = {
            "ERROR": self.logger.error,
            "WARNING": self.logger.warning,
            "DEBUG": self.logger.debug,
        }.get(level, self.logger.info)
        write(entry)

    # ---------------- Manejo de cliente ---------------- #
    def handle_client(self, conn: socket.socket, addr: tuple) -> None:
        try:
            # Sin esto, un cliente silencioso cuelga el hilo indefinidamente
            conn.settimeout(self._CLIENT_TIMEOUT)

            body = self._read_request(conn)
            payload = json.loads(body.decode("utf-8"))

            entries = payload if isinstance(payload, list) else [payload]
            if not entries or len(entries) > self._MAX_BATCH:
                raise ValueError("Lote vacío o demasiado grande")

            logged = 0
            for item in entries:
                if not isinstance(item, dict):
                    raise ValueError("El JSON debe ser un objeto")
                level = self._normalize_level(item.get("level"))
                tag = self._sanitize(str(item.get("tag") or "APP"))[:500]
                message = self._sanitize(str(item.get("message") or ""))[: self.max_body]
                self._write_entry(level, f"[{tag}] {message}")
                print(f"[{level}] [{tag}] {message}")
                logged += 1

            self._send_response(
                conn, "200 OK",
                f'{{"status":"ok","logged":{logged}}}'.encode("ascii"),
            )

        except socket.timeout:
            self.logger.error("Timeout leyendo de %s", addr)
            self._safe_reject(conn, "408 Request Timeout")
        except ValueError as exc:
            # Incluye json.JSONDecodeError y UnicodeDecodeError
            self.logger.error("Petición inválida de %s: %s", addr, exc)
            self._safe_reject(conn, "400 Bad Request")
        except Exception as exc:
            # Fallo interno (disco, etc.): la culpa no es del cliente
            self.logger.error("Error procesando petición de %s: %s", addr, exc)
            self._safe_reject(conn, "500 Internal Server Error")
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def _safe_reject(self, conn: socket.socket, status: str) -> None:
        try:
            self._send_response(conn, status, b'{"status":"error"}')
        except Exception:
            pass

    # ---------------- Ciclo de vida ---------------- #
    def start(self, blocking: bool = True) -> None:
        if blocking:
            self._run()
        else:
            self.is_running = True
            self._thread = threading.Thread(
                target=self._run, daemon=True, name="LogServer"
            )
            self._thread.start()

    def _run(self) -> None:
        self.is_running = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            self._server_socket = server
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.settimeout(1.0)
            server.bind((self.host, self.port))
            server.listen(5)

            print(f"Servidor de logs en http://{self.host}:{self.port}")

            while self.is_running:
                try:
                    conn, addr = server.accept()
                except socket.timeout:
                    continue
                except OSError:
                    break

                threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr),
                    daemon=True,
                ).start()

        self._server_socket = None

    def stop(self) -> None:
        with self._stop_lock:
            self.is_running = False
            sock = self._server_socket

        if sock is not None:
            try:
                sock.close()
            except Exception:
                pass

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

        print("Servidor detenido")


def main() -> None:
    parser = argparse.ArgumentParser(description="Receptor de logs smalilog")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9999)
    parser.add_argument("--log-file", default="smalilog.log")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    server = LogServer(
        host=args.host,
        port=args.port,
        log_file=args.log_file,
        log_level=logging.DEBUG if args.debug else logging.INFO,
    )

    try:
        server.start(blocking=True)
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()
