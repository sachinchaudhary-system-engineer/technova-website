
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
import os

DATA_FILE = Path(os.getenv("DATA_DIR", "/data")) / "visits.json"

SERVICES = [
    "Cloud Computing",
    "DevOps Automation",
    "Linux Administration",
    "Monitoring and Observability"
]


def read_visits():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        DATA_FILE.write_text('{"visits": 0}')

    return json.loads(DATA_FILE.read_text())


class APIHandler(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        body = json.dumps(data).encode()

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "healthy"})
            return

        if self.path == "/api/services":
            self.send_json(200, {
                "company": "TechNova Solutions",
                "services": SERVICES
            })
            return

        if self.path == "/api/visits":
            try:
                data = read_visits()
                data["visits"] += 1
                DATA_FILE.write_text(json.dumps(data))
                self.send_json(200, data)
            except (OSError, ValueError):
                self.send_json(500, {"error": "Data unavailable"})
            return

        self.send_json(404, {"error": "Not found"})

    def log_message(self, fmt, *args):
        print("%s - %s" % (
            self.address_string(), fmt % args
        ), flush=True)


port = int(os.getenv("PORT", "5000"))
HTTPServer(("0.0.0.0", port), APIHandler).serve_forever()
