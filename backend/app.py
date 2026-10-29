
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import time
import redis

cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
    socket_connect_timeout=2
)

SERVICES = [
    "Cloud Computing",
    "DevOps Automation",
    "Linux Administration",
    "Monitoring and Observability"
]


class APIHandler(BaseHTTPRequestHandler):
    def respond(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.respond(200, {"status": "healthy"})
            return

        if self.path == "/api/services":
            try:
                cached = cache.get("technova:services")

                if cached:
                    result = json.loads(cached)
                    result["cache"] = "HIT"
                else:
                    result = {
                        "company": "TechNova Solutions",
                        "services": SERVICES
                    }
                    cache.setex(
                        "technova:services",
                        60,
                        json.dumps(result)
                    )
                    result["cache"] = "MISS"

                self.respond(200, result)

            except redis.RedisError:
                self.respond(503, {
                    "error": "Cache service unavailable"
                })
            return

        self.respond(404, {"error": "Not found"})

    def log_message(self, fmt, *args):
        print("%s - %s" % (
            self.address_string(), fmt % args
        ), flush=True)


HTTPServer(
    ("0.0.0.0", int(os.getenv("PORT", "5000"))),
    APIHandler
).serve_forever()
