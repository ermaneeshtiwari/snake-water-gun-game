from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from snakeWaterGunGame import snake_water_gun


ROOT = Path(__file__).resolve().parent


def render_game_page(result="Make a choice to play."):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Snake Water Gun</title>
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
      <p id="status">{result}</p>
    </div>

    <a href="/" class="small">Reset</a>

    <footer>
      <p>Simple single-round game - powered by Python.</p>
    </footer>
  </main>
</body>
</html>"""


class SnakeWaterGunHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/":
            self.send_html(render_game_page())
            return

        if parsed_url.path == "/api/play":
            query = parse_qs(parsed_url.query)
            choice = query.get("choice", [""])[0]
            self.send_html(render_game_page(snake_water_gun(choice)))
            return

        if parsed_url.path == "/style.css":
            css = (ROOT / "style.css").read_text(encoding="utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.end_headers()
            self.wfile.write(css.encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Not found")

    def send_html(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), SnakeWaterGunHandler)
    print("Snake Water Gun running at http://127.0.0.1:8000")
    server.serve_forever()
