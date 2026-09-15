from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class H(BaseHTTPRequestHandler):
    def log_message(self, *args):
        return
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"ok":true}\n')

HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), H).serve_forever()
