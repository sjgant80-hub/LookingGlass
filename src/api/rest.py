"""REST API for BlockArray operations."""
import json
from http.server import BaseHTTPRequestHandler


def create_app(system):
    """Create request handler bound to system."""

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith("/value"):
                params = _parse_qs(self.path)
                x, y, z = int(params["x"]), int(params["y"]), int(params["z"])
                arr = list(system.arrays.values())[0]
                val = arr.get(x, y, z)
                self._json({"value": val})
            elif self.path == "/status":
                self._json(system.status())
            else:
                self._json({"error": "not found"}, 404)

        def do_POST(self):
            body = self._read_body()
            if self.path == "/value":
                arr = list(system.arrays.values())[0]
                arr.set(body["x"], body["y"], body["z"], body["v"])
                self._json({"ok": True})
            elif self.path == "/template/create":
                d = tuple(body.get("dims", [10, 10, 10]))
                system.create_block_array(body["name"], d)
                self._json({"created": body["name"]})
            else:
                self._json({"error": "not found"}, 404)

        def _json(self, data, code=200):
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        def _read_body(self):
            length = int(self.headers.get("Content-Length", 0))
            return json.loads(self.rfile.read(length))

    return Handler


def _parse_qs(path):
    qs = path.split("?", 1)[-1] if "?" in path else ""
    params = {}
    for part in qs.split("&"):
        if "=" in part:
            k, v = part.split("=", 1)
            params[k] = v
    return params
