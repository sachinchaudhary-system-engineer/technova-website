
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/services":
            data = {
                "company": "TechNova Solutions",
                "services": [
                    "Cloud Computing",
                    "DevOps Automation",
                    "Linux Administration",
                    "Monitoring and Observability"
                ]
            }

            body = json.dumps(data).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))

HTTPServer(("0.0.0.0", 5000), APIHandler).serve_forever()
