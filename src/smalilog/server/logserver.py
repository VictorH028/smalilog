#!/usr/bin/env python3
"""
Servidor TCP/HTTP ligero para recepción y registro de logs en formato JSON.

Este módulo expone la clase LogServer, pensada para ser usada desde el CLI
(smalilog.main) o programáticamente.
"""

import json
import logging
import socket
import threading
from typing import Optional


class LogServer:
    """Servidor TCP/HTTP ligero para recepción y registro de logs en formato JSON."""

    MAX_HEADERS: int = 16 * 1024
    MAX_BODY: int = 1024 * 1024

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 9999,
        log_file: str = "app_logs.txt",
        log_level: int = logging.INFO,
    ) -> None:
        self.host = host
        self.port = port
        self.log_file = log_file
        self.is_running = False
        self._server_socket: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None

        self.logger = logging.getLogger("smalilog.LogServer")
        self.logger.setLevel(log_level)
        self.logger.propagate = False

        if not self.logger.handlers:
            handler = logging.FileHandler(self.log_file, encoding="utf-8")
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    # ---------------- HTTP helpers ---------------- #
    def _send_response(self, conn: socket.socket, status: str, body: bytes = b"") -> None:
        response = (
            f"HTTP/1.1 {status}\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("ascii") + body
        conn.sendall(response)

    def _read_request(self, conn: socket.socket) -> tuple[str, str, bytes]:
        data = b""
        while b"\r\n\r\n" not in data:
            chunk = conn.recv(4096)
            if not chunk:
                raise ValueError("Conexión cerrada")
            data += chunk
            if len(data) > self.MAX_HEADERS:
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
            if name.lower() == "content-length":
                try:
                    content_length = int(value.strip())
                except ValueError:
                    raise ValueError("Content-Length inválido")
                break

        if content_length is None:
            raise ValueError("Falta Content-Length")
        if content_length < 0:
            raise ValueError("Content-Length negativo")
        if content_length > self.MAX_BODY:
            raise ValueError("Cuerpo demasiado grande")

        while len(body) < content_length:
            chunk = conn.recv(4096)
            if not chunk:
                raise ValueError("Cuerpo HTTP incompleto")
            body += chunk

        return method, path, body[:content_length]

    # ---------------- Manejo de cliente ---------------- #
    def handle_client(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        try:
            _, _, body = self._read_request(conn)
            log_data = json.loads(body.decode("utf-8"))
            if not isinstance(log_data, dict):
                raise ValueError("El JSON debe ser un objeto")

            level = str(log_data.get("level", "INFO"))[:100]
            tag = str(log_data.get("tag", "APP"))[:500]
            message = str(log_data.get("message", ""))[: self.MAX_BODY]

            log_entry = f"[{tag}] {message}"

            match level:
                case "ERROR":
                    self.logger.error(log_entry)
                case "WARNING":
                    self.logger.warning(log_entry)
                case "DEBUG":
                    self.logger.debug(log_entry)
                case _:
                    self.logger.info(log_entry)

            self._send_response(conn, "200 OK", b"OK")
            print(f"[{level}] [{tag}] {message}")

        except Exception as exc:
            self.logger.error("Error procesando petición de %s: %s", addr, exc)
            print(f"Error de {addr}: {exc}")
            try:
                self._send_response(conn, "400 Bad Request")
            except Exception:
                pass
        finally:
            try:
                conn.close()
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
                except Exception as exc:
                    if self.is_running:
                        print(f"Error en el loop del servidor: {exc}")
                    break

                threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr),
                    daemon=True,
                ).start()

        self._server_socket = None

    def stop(self) -> None:
        self.is_running = False
        if self._server_socket is not None:
            try:
                self._server_socket.close()
            except Exception:
                pass
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        print("Servidor detenido")
