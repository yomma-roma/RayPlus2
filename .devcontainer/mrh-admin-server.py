#!/usr/bin/env python3

import base64
import hmac
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ADMIN_DIRECTORY = "/opt/mrh-admin"
DEFAULT_ADMIN_USERNAME = "olivia"
DEFAULT_ADMIN_PASSWORD = "olivia@olivia"
LISTEN_HOST = os.getenv("MRH_ADMIN_HOST", "0.0.0.0")
LISTEN_PORT = int(os.getenv("MRH_ADMIN_PORT", "8080"))


def _build_auth_token():
    username = os.getenv("MRH_ADMIN_USERNAME", DEFAULT_ADMIN_USERNAME)
    password = os.getenv("MRH_ADMIN_PASSWORD", DEFAULT_ADMIN_PASSWORD)
    return base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")


class AdminAuthHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ADMIN_DIRECTORY, **kwargs)

    def _is_authorized(self):
        authorization = self.headers.get("Authorization", "")
        if not authorization.startswith("Basic "):
            return False
        presented_token = authorization[6:].strip()
        return hmac.compare_digest(presented_token, _build_auth_token())

    def _request_auth(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="MRH Admin Panel", charset="UTF-8"')
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Authentication required.")

    def do_GET(self):
        if not self._is_authorized():
            self._request_auth()
            return
        super().do_GET()

    def do_HEAD(self):
        if not self._is_authorized():
            self._request_auth()
            return
        super().do_HEAD()


if __name__ == "__main__":
    username = os.getenv("MRH_ADMIN_USERNAME", DEFAULT_ADMIN_USERNAME)
    password = os.getenv("MRH_ADMIN_PASSWORD", DEFAULT_ADMIN_PASSWORD)
    if username == DEFAULT_ADMIN_USERNAME or password == DEFAULT_ADMIN_PASSWORD:
        print(
            "WARNING: Default admin credential detected. Set MRH_ADMIN_USERNAME and MRH_ADMIN_PASSWORD to override.",
            file=sys.stderr,
            flush=True,
        )
    server = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), AdminAuthHandler)
    server.serve_forever()
