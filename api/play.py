import random
from html import escape
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse, urlencode

EMOJI  = {"S": "\U0001f40d", "W": "\U0001f4a7", "G": "\U0001f52b"}
NAME   = {"S": "Snake",      "W": "Water",      "G": "Gun"}
WINS   = {("S", "W"), ("W", "G"), ("G", "S")}
REASON = {
    ("S", "W"): "Snake ne Water pee liya! \U0001f40d\U0001f4a7",
    ("W", "G"): "Water ne Gun bujha diya! \U0001f4a7\U0001f52b",
    ("G", "S"): "Gun ne Snake ko maara! \U0001f52b\U0001f40d",
}

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
.subtitle { color: #666; font-size: 0.85rem; margin-bottom: 1.8rem; }
.name-form { display: flex; flex-direction: column; gap: 1rem; margin-top: 1rem; }
.name-input {
  background: #1a2a50;
  border: 2px solid #2a3a70;
  color: #eee;
  padding: 0.8rem 1.2rem;
  border-radius: 10px;
  font-size: 1.1rem;
  outline: none;
  text-align: center;
}
.name-input:focus { border-color: #e94560; }
.btn-primary {
  background: #e94560;
  border: none;
  color: white;
  padding: 0.8rem;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-primary:hover { background: #c73652; }
.scoreboard {
  display: flex;
  justify-content: center;
  gap: 0.8rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.score-box {
  background: #0f1c36;
  border-radius: 10px;
  padding: 0.5rem 1rem;
  min-width: 70px;
}
.score-box .score-val { font-size: 1.5rem; font-weight: bold; }
.score-box .score-lbl { font-size: 0.7rem; color: #888; }
.score-win  .score-val { color: #4caf50; }
.score-lose .score-val { color: #e94560; }
.score-tie  .score-val { color: #f0c040; }
.score-rnd  .score-val { color: #64b5f6; }
.player-tag { color: #aaa; font-size: 0.9rem; margin-bottom: 1rem; }
.player-tag strong { color: #e94560; }
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
.battle { display: flex; align-items: center; justify-content: center; gap: 1rem; margin: 1rem 0; }
.fighter { display: flex; flex-direction: column; align-items: center; gap: 0.3rem; flex: 1; }
.fighter .emoji { font-size: 4rem; animation: pop 0.5s ease; }
.fighter .fname { font-size: 0.85rem; color: #aaa; }
.fighter .ftag  { font-size: 0.72rem; color: #555; }
.vs { font-size: 1.3rem; font-weight: bold; color: #444; flex-shrink: 0; }
@keyframes pop {
  0%   { transform: scale(0.4); opacity: 0; }
  70%  { transform: scale(1.25); }
  100% { transform: scale(1); opacity: 1; }
}
.result-banner {
  border-radius: 12px;
  padding: 0.8rem 1.2rem;
  margin: 0.5rem 0 1rem;
}
.result-label { font-size: 1.3rem; font-weight: bold; margin-bottom: 0.3rem; }
.reason { font-size: 0.9rem; color: #ccc; }

/* countdown bar */
.countdown-wrap { margin: 0.8rem 0 0.4rem; }
.countdown-bar-bg {
  background: #0f1c36;
  border-radius: 99px;
  height: 6px;
  overflow: hidden;
  margin-bottom: 0.4rem;
}
.countdown-bar {
  height: 6px;
  border-radius: 99px;
  background: #64b5f6;
  width: 100%;
  animation: shrink 2s linear forwards;
}
@keyframes shrink { from { width: 100%; } to { width: 0%; } }
.countdown-txt { font-size: 0.8rem; color: #666; }

.actions { display: flex; gap: 0.6rem; justify-content: center; flex-wrap: wrap; margin-top: 0.5rem; }
.btn-sm {
  background: #1a2a50;
  border: 1px solid #2a3a70;
  color: #eee;
  padding: 0.55rem 1.1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
  display: inline-block;
}
.btn-sm:hover { background: #e94560; border-color: #e94560; }
.btn-end { border-color: #f0c040; color: #f0c040; }
.btn-end:hover { background: #f0c040 !important; color: #000 !important; }
.final-wrap { margin-top: 1rem; }
.final-title { font-size: 1.3rem; color: #f0c040; margin-bottom: 1rem; }
.final-grid { display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.2rem; }
.final-box { background: #0f1c36; border-radius: 12px; padding: 1rem 1.5rem; min-width: 80px; }
.final-box .fval { font-size: 2rem; font-weight: bold; }
.final-box .flbl { font-size: 0.75rem; color: #888; margin-top: 0.2rem; }
.verdict { font-size: 1.1rem; margin: 0.5rem 0 1rem; }
.new-game-btn {
  background: #e94560;
  border: none;
  color: white;
  padding: 0.7rem 2rem;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  margin-top: 0.5rem;
}
.new-game-btn:hover { background: #c73652; }
footer { margin-top: 1.5rem; color: #333; font-size: 0.75rem; }
"""


def play_round(user):
    comp = random.choice(list(NAME.keys()))
    if user == comp:
        outcome, label, color = "tie",  "Tie! \U0001f91d",            "#f0c040"
        reason = "Dono ne same choice kiya!"
    elif (user, comp) in WINS:
        outcome, label, color = "win",  "Aap Jeete! \U0001f389",     "#4caf50"
        reason = REASON[(user, comp)]
    else:
        outcome, label, color = "lose", "Computer Jeeta! \U0001f916", "#e94560"
        reason = REASON[(comp, user)]
    return comp, outcome, label, color, reason


def page(body, head_extra="", title="Snake Water Gun"):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{title}</title>
  <style>{CSS}</style>
  {head_extra}
</head>
<body><div class="card">{body}</div></body>
</html>"""


def name_screen():
    body = """
    <h1>\U0001f40d Snake Water Gun \U0001f52b</h1>
    <p class="subtitle">Apna naam enter karo aur game shuru karo!</p>
    <form class="name-form" action="/api/play" method="get">
      <input class="name-input" type="text" name="name"
             placeholder="Tumhara naam..." required autofocus maxlength="20" />
      <button class="btn-primary" type="submit">&#x25B6; Game Shuru Karo</button>
    </form>
    <footer>Snake beats Water &bull; Water beats Gun &bull; Gun beats Snake</footer>
    """
    return page(body)


def choice_screen(name, wins, losses, ties):
    rounds = wins + losses + ties
    params = urlencode({"name": name, "wins": wins, "losses": losses, "ties": ties})
    body = f"""
    <h1>\U0001f40d Snake Water Gun \U0001f52b</h1>
    <p class="player-tag">Namaste, <strong>{escape(name)}</strong>! \U0001f44b</p>
    <div class="scoreboard">
      <div class="score-box score-rnd">
        <div class="score-val">{rounds}</div><div class="score-lbl">Rounds</div>
      </div>
      <div class="score-box score-win">
        <div class="score-val">{wins}</div><div class="score-lbl">Jeete</div>
      </div>
      <div class="score-box score-lose">
        <div class="score-val">{losses}</div><div class="score-lbl">Haare</div>
      </div>
      <div class="score-box score-tie">
        <div class="score-val">{ties}</div><div class="score-lbl">Tie</div>
      </div>
    </div>
    <p class="subtitle">Apna choice karo:</p>
    <form class="choices" action="/api/play" method="get">
      <input type="hidden" name="name" value="{escape(name)}" />
      <input type="hidden" name="wins" value="{wins}" />
      <input type="hidden" name="losses" value="{losses}" />
      <input type="hidden" name="ties" value="{ties}" />
      <button class="btn" name="choice" value="S">\U0001f40d<span class="lbl">Snake</span></button>
      <button class="btn" name="choice" value="W">\U0001f4a7<span class="lbl">Water</span></button>
      <button class="btn" name="choice" value="G">\U0001f52b<span class="lbl">Gun</span></button>
    </form>
    <div class="actions">
      <a class="btn-sm btn-end" href="/api/play?{params}&end=1">\U0001f3c1 Game Khatam Karo</a>
    </div>
    <footer>Snake beats Water &bull; Water beats Gun &bull; Gun beats Snake</footer>
    """
    return page(body)


def result_screen(name, user, comp, outcome, label, color, reason, wins, losses, ties):
    rounds = wins + losses + ties
    next_url = "/api/play?" + urlencode({"name": name, "wins": wins, "losses": losses, "ties": ties})
    end_url  = "/api/play?" + urlencode({"name": name, "wins": wins, "losses": losses, "ties": ties, "end": 1})

    # Auto-redirect after 2 seconds; clicking either button cancels it
    head_extra = f"""
    <script>
      var timer = setTimeout(function() {{
        window.location.href = "{next_url}";
      }}, 2000);
      function cancel() {{ clearTimeout(timer); }}
    </script>"""

    body = f"""
    <h1>\U0001f40d Snake Water Gun \U0001f52b</h1>
    <p class="player-tag">Round <strong>{rounds}</strong> &mdash; <strong style="color:#e94560">{escape(name)}</strong></p>
    <div class="scoreboard">
      <div class="score-box score-rnd">
        <div class="score-val">{rounds}</div><div class="score-lbl">Rounds</div>
      </div>
      <div class="score-box score-win">
        <div class="score-val">{wins}</div><div class="score-lbl">Jeete</div>
      </div>
      <div class="score-box score-lose">
        <div class="score-val">{losses}</div><div class="score-lbl">Haare</div>
      </div>
      <div class="score-box score-tie">
        <div class="score-val">{ties}</div><div class="score-lbl">Tie</div>
      </div>
    </div>
    <div class="battle">
      <div class="fighter">
        <div class="emoji">{EMOJI[user]}</div>
        <div class="fname">{NAME[user]}</div>
        <div class="ftag">{escape(name)}</div>
      </div>
      <div class="vs">VS</div>
      <div class="fighter">
        <div class="emoji">{EMOJI[comp]}</div>
        <div class="fname">{NAME[comp]}</div>
        <div class="ftag">Computer</div>
      </div>
    </div>
    <div class="result-banner" style="background:{color}22; border:2px solid {color}">
      <div class="result-label" style="color:{color}">{label}</div>
      <div class="reason">{reason}</div>
    </div>
    <div class="countdown-wrap">
      <div class="countdown-bar-bg"><div class="countdown-bar"></div></div>
      <div class="countdown-txt">2 second mein agli round shuru hogi...</div>
    </div>
    <div class="actions">
      <a class="btn-sm" href="{next_url}" onclick="cancel()">\U0001f504 Abhi Khelo</a>
      <a class="btn-sm btn-end" href="{end_url}" onclick="cancel()">\U0001f3c1 Game Khatam Karo</a>
    </div>
    <footer>Snake beats Water &bull; Water beats Gun &bull; Gun beats Snake</footer>
    """
    return page(body, head_extra, f"Round {rounds} - {name}")


def final_screen(name, wins, losses, ties):
    rounds = wins + losses + ties
    if rounds == 0:
        verdict, vcolor = "Koi round nahi khela!", "#888"
    elif wins > losses:
        verdict, vcolor = f"\U0001f3c6 {escape(name)} ne jeeta! Bahut badhiya!", "#4caf50"
    elif losses > wins:
        verdict, vcolor = "\U0001f916 Computer ne jeeta! Agli baar try karo!", "#e94560"
    else:
        verdict, vcolor = "\U0001f91d Barabar raha! Koi nahi jeeta!", "#f0c040"

    win_pct = round(wins / rounds * 100) if rounds else 0
    body = f"""
    <h1>\U0001f3c1 Game Khatam!</h1>
    <p class="subtitle" style="color:#f0c040; font-size:1rem; margin-bottom:1.2rem;">{escape(name)} ka Final Score</p>
    <div class="final-wrap">
      <div class="final-grid">
        <div class="final-box"><div class="fval" style="color:#64b5f6">{rounds}</div><div class="flbl">Total Rounds</div></div>
        <div class="final-box"><div class="fval" style="color:#4caf50">{wins}</div><div class="flbl">Jeete</div></div>
        <div class="final-box"><div class="fval" style="color:#e94560">{losses}</div><div class="flbl">Haare</div></div>
        <div class="final-box"><div class="fval" style="color:#f0c040">{ties}</div><div class="flbl">Tie</div></div>
        <div class="final-box"><div class="fval" style="color:#ab47bc">{win_pct}%</div><div class="flbl">Win Rate</div></div>
      </div>
      <div class="verdict" style="color:{vcolor}">{verdict}</div>
      <a class="new-game-btn" href="/api/play">\U0001f504 Naya Game Shuru Karo</a>
    </div>
    <footer style="margin-top:1.5rem">Snake beats Water &bull; Water beats Gun &bull; Gun beats Snake</footer>
    """
    return page(body, title=f"Final Score - {name}")


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = parse_qs(urlparse(self.path).query)
        g = lambda k, d="": qs.get(k, [d])[0]

        name   = g("name").strip()
        choice = g("choice").strip().upper()
        end    = g("end")
        wins   = int(g("wins",   "0"))
        losses = int(g("losses", "0"))
        ties   = int(g("ties",   "0"))

        if not name:
            html = name_screen()
        elif end:
            html = final_screen(name, wins, losses, ties)
        elif choice in NAME:
            comp, outcome, label, color, reason = play_round(choice)
            if outcome == "win":    wins   += 1
            elif outcome == "lose": losses += 1
            else:                   ties   += 1
            html = result_screen(name, choice, comp, outcome,
                                 label, color, reason, wins, losses, ties)
        else:
            html = choice_screen(name, wins, losses, ties)

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))
