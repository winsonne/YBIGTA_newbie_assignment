from __future__ import annotations

from typing import Optional


def build_request(host: str, path: str) -> bytes:
    """
    HTTP GET 요청 메시지를 바이트 형태로 생성합니다.
    """
    if not path.startswith("/"):
        path = "/" + path

    req = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )

    return req.encode("utf-8")


def send_and_recv(sock, request: bytes, max_bytes: int) -> bytes:
    
    sock.sendall(request)

    chunks: list[bytes] = []
    total = 0
    while True:
        data = sock.recv(4096)
        if not data:
            break
        chunks.append(data)
        total += len(data)
        if total > max_bytes:
            break
    return b"".join(chunks)


def parse_status_and_preview(raw: bytes, max_preview: int = 200) -> tuple[Optional[int], str, Optional[str]]:
    """
    서버의 Raw 응답 데이터를 분석하여 상태 코드와 본문 미리보기를 추출합니다. 
    
    요구사항:
    1. 헤더와 바디를 구분하는 CRLF 2번(b"\\r\\n\\r\\n")의 위치를 찾으세요. 
    2. 헤더 영역을 decode한 뒤, Status Line(첫 줄)에서 상태 코드를 추출하세요. 
    3. 바디 영역에서 max_preview 만큼의 데이터를 decode하여 반환하세요. 
    4. 규격에 맞지 않는 데이터가 들어올 경우 적절한 에러 메시지를 반환하세요. 
    """
    boundary = raw.find(b"\r\n\r\n")

    if boundary == -1:
        return None, "", "Invalid HTTP response: header/body boundary not found"

    header_bytes = raw[:boundary]
    body_bytes = raw[boundary + 4:]

    try:
        header = header_bytes.decode("iso-8859-1")
    except UnicodeDecodeError as e:
        return None, "", f"Invalid HTTP header encoding: {e}"

    header_lines = header.split("\r\n")

    if not header_lines or not header_lines[0]:
        return None, "", "Invalid HTTP response: missing status line"

    status_line = header_lines[0]
    status_parts = status_line.split()

    if len(status_parts) < 2:
        return None, "", "Invalid HTTP response: malformed status line"

    if not status_parts[0].startswith("HTTP/"):
        return None, "", "Invalid HTTP response: invalid HTTP version"

    try:
        status_code = int(status_parts[1])
    except ValueError:
        return None, "", "Invalid HTTP response: status code is not an integer"

    if status_code < 100 or status_code > 999:
        return None, "", "Invalid HTTP response: invalid status code"

    preview = body_bytes[:max_preview].decode(
        "utf-8",
        errors="replace"
    )

    error = None

    return status_code, preview, error