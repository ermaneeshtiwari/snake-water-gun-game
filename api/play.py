import random
from html import escape
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

EMOJI = {"S": "\U0001f40d", "W": "\U0001f4a7", "G": "\U0001f52b"}
NAME  = {"S": "Snake",      "W": "Water",      "G": "Gun"}

REASON = {
    ("S", "W"): "Snake ne Water pee liya!",
    ("W", "G"): "Water ne Gun bujha diya!",
    ("G", "S"): "Gun ne Snake ko maara!",
}

WINS = {("S", "W"), ("W", "G"), ("G", "S")}


def play(user):
    user = user.strip().upper()
    if user not in NAME:
        return None
    comp = random.choice(list(NAME.keys()))
    if user == comp:
        outcome, label, color = "tie",  "It's a Tie! \U0001f91d", "#f0c040"
        reason = "Dono ne same choose kiya!"
    elif (user, comp) in WINS:
        outcome, label, color = "win",  "Aap Jeete! \U0001f389",  "#4caf50"
        reason = REASON[(user, comp)]
    else:
        outcome, label, color = "lose", "Computer Jeeta! \U0001f916", "#e94560"
        reason = REASON[(comp, user)]
    return dict(user=user, comp=comp, outcome=outcome,
                label=label, color=color, reason=reason)


CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Segoe UI', Arial, sans-serif;
  background: #0d0d1a;
  color: #eee;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}
.card {
  background: #16213e;
  border-radius: 16px;
  padding: 2rem 2.5rem;
  max-width: 520px;
  width: 100%;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  text-align: center;
}
h1 { color: #e94560; font-size: 1.8rem; margin-bottom: 0.3rem; }
.subtitle { color: #888; font-size: 0.9rem; margin-bottom: 1.8rem; }

/* choice buttons */
.choices { display: flex; gap: 0.8rem; justify-content: center; flex-wrap: wrap; margin-bottom: 1.5rem; }
.btn {
  background: #1a2a50;
  border: 2px solid #2a3a70;
  color: #eee;
  padding: 0.8rem 1.4rem;
  border-radius: 12px;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex; flex-direction: column; align-items: center; gap: 0.2rem;
}
.btn span.lbl { font-size: 0.75rem; color: #aaa; }
.btn:hover { background: #e94560; border-color: #e94560; transform: translateY(-3px); }

/* battle scene */
.battle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin: 1.5rem 0;
}
.fighter {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  flex: 1;
}
.fighter .emoji {
  font-size: 4rem;
  animation: bounce 0.6s ease;
}
.fighter .fname { font-size: 0.85rem; color: #aaa; }
.fighter .ftag  { font-size: 0.75rem; color: #666; }
.vs {
  font-size: 1.4rem;
  font-weight: bold;
  color: #444;
  flex-shrink: 0;
}
@keyframes bounce {
  0%   { transform: scale(0.5); opacity: 0; }
  60%  { transform: scale(1.2); }
  100% { transform: scale(1);   opacity: 1; }
}

/* result banner */
.result-banner {
  border-radius: 12px;
  padding: 1rem 1.5rem;
  margin: 0.5rem 0 1rem;
}
.result-banner .result-label {
  font-size: 1.4rem;
  font-weight: bold;
  margin-bottom: 0.3rem;
}
.result-banner .reason {
  font-size: 0.95rem;
  color: #ccc;
}

.play-again {
  display: inline-block;
  margin-top: 0.5rem;
  color: #888;
  font-size: 0.85rem;
  text-decoration: none;
}
.play-again:hover { color: #e94560; }
footer { margin-top: 1.5rem; color: #444; font-size: 0.75rem; }
"""


def build_page(result=None):
    if result:
        battle_html = f"""
      <div class="battle">
        <div class="fighter">
          <div class="emoji">{EMOJI[result['user']]}</div>
          <div class="fname">{NAME[result['user']]}</div>
          <div class="ftag">Aap</div>
        </div>
        <div class="vs">VS</div>
        <div class="fighter">
          <div class="emoji">{EMOJI[result['comp']]}</div>
          <div class="fname">{NAME[result['comp']]}</div>
          <div class="ftag">Computer</div>
        </div>
      </div>
      <div class="result-banner" style="background:{result['color']}22; border: 2px solid {result['color']}">
        <div class="result-label" style="color:{result['color']}">{result['label']}</div>
        <div class="reason">{result['reason']}</div>
      </div>"""
    else:
        battle_html = """
      <div style="color:#555; font-size:3rem; margin:1.5rem 0;">&#x2753;</div>
      <p style="color:#666; margin-bottom:1rem;">Apna choice karo aur game shuru karo!</p>"""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Snake Water Gun</title>
  <style>{CSS}</style>
</head>
<body>
  <div class="card">
    <h1>&#x1f40d; Snake Water Gun &#x1f52b;</h1>
    <p class="subtitle">Snake beats Water &bull; Water beats Gun &bull; Gun beats Snake</p>

    <form class="choices" action="/api/play" method="get">
      <button class="btn" name="choice" value="S" type="submit">
        &#x1f40d;<span class="lbl">Snake</span>
      </button>
      <button class="btn" name="choice" value="W" type="submit">
        &#x1f4a7;<span class="lbl">Water</span>
      </button>
      <button class="btn" name="choice" value="G" type="submit">
        &#x1f52b;<span class="lbl">Gun</span>
      </button>
    </form>
{battle_html}
    <a href="/api/play" class="play-again">&#x21ba; Dobara Khelo</a>
    <footer>Powered by Python &mdash; Single round game</footer>
  </div>
</body>
</html>"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        choice = query.get("choice", [""])[0]
        result = play(choice) if choice else None
        html = build_page(result)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))
