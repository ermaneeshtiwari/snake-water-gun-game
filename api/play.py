from html import escape
from http.server import BaseHTTPRequestHandler
from pathlib import Path
import sys
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from snakeWaterGunGame import snake_water_gun


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        choice = query.get("choice", [""])[0]
        result = snake_water_gun(choice)

        html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Snake Water Gun Result</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <main class="container">
    <h1>Snake Water Gun</h1>
    <p class="rules">Choose one: <strong>S</strong> (Snake), <strong>W</strong> (Water), <strong>G</strong> (Gun)</p>

    <form class="choices" action="/api/play" method="get">
      <button name="choice" value="S" type="submit">Snake (S)</button>
      <button name="choice" value="W" type="submit">Water (W)</button>
      <button name="choice" value="G" type="submit">Gun (G)</button>
    </form>

    <div class="result">
      <p id="status">{escape(result)}</p>
    </div>

    <a href="/" class="small">Reset</a>

    <footer>
      <p>Simple single-round game - powered by Python.</p>
    </footer>
  </main>
</body>
</html>"""

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))
