#!/usr/bin/env python3
"""
Overhead — local helper for the flight tracker.

Serves index.html and fetches the flight data for it, because the flight
feeds don't allow web pages to call them directly. Runs the same way on a
Windows/Mac laptop or a Raspberry Pi. Needs only Python 3 (no installs).

    python server.py            then open  http://localhost:8000
    python server.py --port 8080
"""
import argparse
import json
import os
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "overhead-tracker (https://github.com/rgarabedian16/flight-tracker)"

SOURCES = os.environ.get("OVERHEAD_SOURCES", "").split(",") if os.environ.get("OVERHEAD_SOURCES") else [
    "https://api.adsb.lol/v2/lat/{lat}/lon/{lon}/dist/{dist}",
    "https://api.airplanes.live/v2/point/{lat}/{lon}/{dist}",
    "https://opendata.adsb.fi/api/v2/lat/{lat}/lon/{lon}/dist/{dist}",
]
ROUTESET = os.environ.get("OVERHEAD_ROUTESET", "https://api.adsb.lol/api/0/routeset")


def fetch(url, data=None, timeout=8):
    req = urllib.request.Request(url, data=data, headers={
        "User-Agent": UA, "Accept": "application/json",
        **({"Content-Type": "application/json"} if data else {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=HERE, **kw)

    def log_message(self, fmt, *args):  # keep the console quiet except for errors
        pass

    def send_json(self, status, body):
        if isinstance(body, (dict, list)):
            body = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/api/aircraft":
            q = parse_qs(u.query)
            try:
                lat = float(q["lat"][0]); lon = float(q["lon"][0])
                dist = max(1, min(250, round(float(q.get("dist", ["10"])[0]))))
                assert abs(lat) <= 90 and abs(lon) <= 180
            except Exception:
                return self.send_json(400, {"error": "bad location"})
            for src in SOURCES:
                try:
                    status, body = fetch(src.format(lat=f"{lat:.4f}", lon=f"{lon:.4f}", dist=dist))
                    if status == 200:
                        return self.send_json(200, body)
                except Exception as e:
                    print(f"  source failed: {src.split('/')[2]} ({e})")
            return self.send_json(502, {"error": "all flight sources unavailable"})
        if u.path == "/api/health":
            return self.send_json(200, {"ok": True})
        if u.path in ("", "/"):
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/routeset":
            return self.send_json(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length") or 0)
        if length > 20000:
            return self.send_json(413, {"error": "too large"})
        try:
            status, body = fetch(ROUTESET, data=self.rfile.read(length))
            return self.send_json(status, body)
        except urllib.error.HTTPError as e:
            return self.send_json(e.code, {"error": "route lookup failed"})
        except Exception:
            return self.send_json(502, {"error": "route lookup unavailable"})


def main():
    ap = argparse.ArgumentParser(description="Overhead flight tracker helper")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="127.0.0.1", help="use 0.0.0.0 to open it from other devices on your Wi-Fi")
    a = ap.parse_args()
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"Overhead is running — open http://localhost:{a.port} in your browser (Ctrl+C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
