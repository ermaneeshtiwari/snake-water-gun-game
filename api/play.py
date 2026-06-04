import random
from html import escape
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse


def snake_water_gun(user_choice):
    user_choice = user_choice.strip().upper()
    choices = {"S": 1, "W": 0, "G": -1}
    choice_names = {"S": "Snake", "W": "Water", "G": "Gun"}
    computer_choice = random.choice(list(choices.keys()))

    if user_choice not in choices:
        return "Invalid choice! Please choose S, W, or G."

    if user_choice == computer_choice:
        result = "It's a tie!"
    elif (
        (user_choice == "S" and computer_choice == "W")
        or (user_choice == "W" and computer_choice == "G")
        or (user_choice == "G" and computer_choice == "S")
    ):
        result = "You win!"
    else:
        result = "Computer wins!"

    return (
        f"You chose {choice_names[user_choice]}. "
        f"Computer chose {choice_names[computer_choice]}. "
        f"{result}"
    )


CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: Arial, sans-serif;
  background: #1a1a2e;
  color: #eee;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
.container {
  text-align: center;
  background: #16213e;
  padding: 2rem 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
  max-width: 480px;
  width: 90%;
}
h1 { color: #e94560; margin-bottom: 0.5rem; font-size: 2rem; }
.rules { color: #aaa; margin-bottom: 1.5rem; }
.choices { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 1.5rem; }
button {
  background: #e94560;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
button:hover { background: #c73652; }
.result {
  background: #0f3460;
  padding: 1rem;
  border-radius: 8px;
  min-height: 3.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
#status { margin: 0; font-size: 1.1rem; }
.small { display: inline-block; margin-top: 1rem; color: #aaa; font-size: 0.85rem; text-decoration: none; }
.small:hover { color: #e94560; }
footer { margin-top: 1.5rem; color: #555; font-size: 0.8rem; }
"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/style.css":
            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.end_headers()
            self.wfile.write(CSS.encode("utf-8"))
            return

        query = parse_qs(parsed.query)
        choice = query.get("choice", [""])[0]
        result = snake_water_gun(choice) if choice else "Make a choice to play."

        html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Snake Water Gun</title>
  <style>{CSS}</style>
</head>
<body>
  <main class="container">
    <h1>Snake Water Gun</h1>
    <p class="rules">Choose one: <strong>S</strong> (Snake), <strong>W</strong> (Water), <strong>G</strong> (Gun)</p>

    <form class="choices" action="/api/play" method="get">
      <button name="choice" value="S" type="submit">&#x1F40D; Snake</button>
      <button name="choice" value="W" type="submit">&#x1F4A7; Water</button>
      <button name="choice" value="G" type="submit">&#x1F52B; Gun</button>
    </form>

    <div class="result">
      <p id="status">{escape(result)}</p>
    </div>

    <a href="/" class="small">Play again</a>

    <footer>
      <p>Simple single-round game &mdash; powered by Python.</p>
    </footer>
  </main>
</body>
</html>"""

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))
