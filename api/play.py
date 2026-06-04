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


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        choice = query.get("choice", [""])[0]
        result = snake_water_gun(choice) if choice else "Make a choice to play."

        html = f"""<!doctype html>
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
