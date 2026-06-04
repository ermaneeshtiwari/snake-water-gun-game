import json
import random
import struct
import zlib
from html import escape
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse, urlencode

EMOJI  = {"S": "\U0001f40d", "W": "\U0001f4a7", "G": "\U0001f52b"}
NAME   = {"S": "Snake",      "W": "Water",      "G": "Gun"}
WINS   = {("S", "W"), ("W", "G"), ("G", "S")}
REASON = {
    ("S", "W"): "Snake drank the Water! \U0001f40d\U0001f4a7",
    ("W", "G"): "Water doused the Gun! \U0001f4a7\U0001f52b",
    ("G", "S"): "Gun shot the Snake! \U0001f52b\U0001f40d",
}

# ---------------------------------------------------------------------------
# PWA assets
# ---------------------------------------------------------------------------

def _make_png(size):
    """Generate a PNG icon: red square centred on dark background."""
    pad  = size // 6
    dark = bytes([13, 13, 26])    # #0d0d1a
    red  = bytes([233, 69, 96])   # #e94560
    dark_row = b'\x00' + dark * size
    mid_row  = b'\x00' + dark * pad + red * (size - 2 * pad) + dark * pad
    raw = dark_row * pad + mid_row * (size - 2 * pad) + dark_row * pad

    def chunk(t, d):
        c = t + d
        return struct.pack('>I', len(d)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    return (
        b'\x89PNG\r\n\x1a\n'
        + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
        + chunk(b'IDAT', zlib.compress(raw, 9))
        + chunk(b'IEND', b'')
    )


ICON_192 = _make_png(192)
ICON_512 = _make_png(512)

MANIFEST = json.dumps({
    "name": "Snake Water Gun",
    "short_name": "SWG",
    "description": "Classic Snake Water Gun hand game — play vs computer!",
    "start_url": "/api/play",
    "display": "standalone",
    "background_color": "#0d0d1a",
    "theme_color": "#e94560",
    "orientation": "portrait-primary",
    "icons": [
        {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
        {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
    ],
}).encode()

SW_JS = b"""
const CACHE = 'swg-v1';

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(['/api/play'])));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => clients.claim())
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    fetch(e.request)
      .then(r => {
        if (r.ok) {
          const clone = r.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return r;
      })
      .catch(() => caches.match(e.request))
  );
});
"""

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

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
  background: #1a2a50; border: 2px solid #2a3a70; color: #eee;
  padding: 0.8rem 1.2rem; border-radius: 10px; font-size: 1.1rem;
  outline: none; text-align: center;
}
.name-input::placeholder { color: #456; }
.name-input:focus { border-color: #e94560; }
.btn-primary {
  background: #e94560; border: none; color: white;
  padding: 0.8rem; border-radius: 10px; font-size: 1rem;
  cursor: pointer; transition: background 0.2s;
}
.btn-primary:hover { background: #c73652; }
.scoreboard {
  display: flex; justify-content: center; gap: 0.8rem;
  margin-bottom: 1.5rem; flex-wrap: wrap;
}
.score-box { background: #0f1c36; border-radius: 10px; padding: 0.5rem 1rem; min-width: 70px; }
.score-box .score-val { font-size: 1.5rem; font-weight: bold; }
.score-box .score-lbl { font-size: 0.7rem; color: #888; }
.score-win  .score-val { color: #4caf50; }
.score-lose .score-val { color: #e94560; }
.score-tie  .score-val { color: #f0c040; }
.score-rnd  .score-val { color: #64b5f6; }
.player-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; }
.player-tag { color: #aaa; font-size: 0.9rem; }
.player-tag strong { color: #e94560; }
.btn-new-player {
  background: transparent; border: 1px solid #2a3a70; color: #888;
  padding: 0.3rem 0.7rem; border-radius: 6px; font-size: 0.75rem;
  cursor: pointer; text-decoration: none; transition: all 0.2s;
}
.btn-new-player:hover { border-color: #e94560; color: #e94560; }
.choices { display: flex; gap: 0.8rem; justify-content: center; flex-wrap: wrap; margin-bottom: 1.5rem; }
.btn {
  background: #1a2a50; border: 2px solid #2a3a70; color: #eee;
  padding: 0.8rem 1.4rem; border-radius: 12px; font-size: 1.5rem;
  cursor: pointer; transition: all 0.2s;
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
.result-banner { border-radius: 12px; padding: 0.8rem 1.2rem; margin: 0.5rem 0 1rem; }
.result-label { font-size: 1.3rem; font-weight: bold; margin-bottom: 0.3rem; }
.reason { font-size: 0.9rem; color: #ccc; }
.countdown-wrap { margin: 0.8rem 0 0.4rem; }
.countdown-bar-bg { background: #0f1c36; border-radius: 99px; height: 6px; overflow: hidden; margin-bottom: 0.4rem; }
.countdown-bar { height: 6px; border-radius: 99px; background: #64b5f6; width: 100%; animation: shrink 2s linear forwards; }
@keyframes shrink { from { width: 100%; } to { width: 0%; } }
.countdown-txt { font-size: 0.8rem; color: #555; }
.actions { display: flex; gap: 0.6rem; justify-content: center; flex-wrap: wrap; margin-top: 0.5rem; }
.btn-sm {
  background: #1a2a50; border: 1px solid #2a3a70; color: #eee;
  padding: 0.55rem 1.1rem; border-radius: 8px; font-size: 0.9rem;
  cursor: pointer; text-decoration: none; transition: all 0.2s; display: inline-block;
}
.btn-sm:hover { background: #e94560; border-color: #e94560; }
.btn-end { border-color: #f0c040; color: #f0c040; }
.btn-end:hover { background: #f0c040 !important; color: #000 !important; }
.final-grid { display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.2rem; }
.final-box { background: #0f1c36; border-radius: 12px; padding: 1rem 1.5rem; min-width: 80px; }
.final-box .fval { font-size: 2rem; font-weight: bold; }
.final-box .flbl { font-size: 0.75rem; color: #888; margin-top: 0.2rem; }
.verdict { font-size: 1.1rem; margin: 0.5rem 0 1.2rem; }
.new-game-btn {
  background: #e94560; border: none; color: white;
  padding: 0.7rem 2rem; border-radius: 10px; font-size: 1rem;
  cursor: pointer; text-decoration: none; display: inline-block;
}
.new-game-btn:hover { background: #c73652; }
.new-player-btn {
  display: inline-block; margin-top: 0.8rem; color: #555;
  font-size: 0.8rem; text-decoration: none; border-bottom: 1px dashed #333;
}
.new-player-btn:hover { color: #e94560; border-color: #e94560; }
.install-banner {
  display: none;
  background: #0f3460; border: 1px solid #1a5276;
  border-radius: 10px; padding: 0.6rem 1rem;
  margin-bottom: 1rem; font-size: 0.85rem;
  align-items: center; justify-content: space-between; gap: 0.5rem;
}
.install-banner.show { display: flex; }
.install-btn {
  background: #e94560; color: white; border: none;
  padding: 0.3rem 0.8rem; border-radius: 6px; font-size: 0.8rem;
  cursor: pointer; white-space: nowrap;
}
footer { margin-top: 1.5rem; color: #333; font-size: 0.75rem; }
"""

PWA_HEAD = """
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#e94560">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Snake Water Gun">
  <link rel="apple-touch-icon" href="/icon-192.png">"""

PWA_SCRIPT = """
  <script>
    // Register service worker
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js');
    }
    // Install banner
    var deferredPrompt;
    window.addEventListener('beforeinstallprompt', function(e) {
      e.preventDefault();
      deferredPrompt = e;
      var banner = document.getElementById('install-banner');
      if (banner) banner.classList.add('show');
    });
    function installApp() {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then(function() { deferredPrompt = null; });
        var banner = document.getElementById('install-banner');
        if (banner) banner.classList.remove('show');
      }
    }
    window.addEventListener('appinstalled', function() {
      var banner = document.getElementById('install-banner');
      if (banner) banner.classList.remove('show');
    });
  </script>"""

INSTALL_BANNER = """
    <div class="install-banner" id="install-banner">
      <span>\U0001f4f2 Install as app on your phone!</span>
      <button class="install-btn" onclick="installApp()">Install</button>
    </div>"""

# ---------------------------------------------------------------------------
# Cookie helpers
# ---------------------------------------------------------------------------

def read_cookie_name(headers):
    cookies = SimpleCookie()
    try:
        cookies.load(headers.get("Cookie", ""))
    except Exception:
        pass
    m = cookies.get("player_name")
    return m.value.strip() if m else ""

def set_cookie_header(name):
    return f"player_name={name}; Path=/; SameSite=Lax"

def clear_cookie_header():
    return "player_name=; Path=/; Max-Age=0; SameSite=Lax"

# ---------------------------------------------------------------------------
# Game logic
# ---------------------------------------------------------------------------

def play_round(user):
    comp = random.choice(list(NAME.keys()))
    if user == comp:
        outcome, label, color = "tie",  "It's a Tie! \U0001f91d",       "#f0c040"
        reason = "Both chose the same!"
    elif (user, comp) in WINS:
        outcome, label, color = "win",  "You Win! \U0001f389",           "#4caf50"
        reason = REASON[(user, comp)]
    else:
        outcome, label, color = "lose", "Computer Wins! \U0001f916",     "#e94560"
        reason = REASON[(comp, user)]
    return comp, outcome, label, color, reason

# ---------------------------------------------------------------------------
# Page builder
# ---------------------------------------------------------------------------

def page(body, head_extra="", title="Snake Water Gun"):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{title}</title>{PWA_HEAD}
  <style>{CSS}</style>
  {head_extra}
</head>
<body>
  <div class="card">
{INSTALL_BANNER}
{body}
  </div>
{PWA_SCRIPT}
</body>
</html>"""

# ---------------------------------------------------------------------------
# Screens
# ---------------------------------------------------------------------------

def name_screen():
    body = """
    <h1>\U0001f40d Snake Water Gun \U0001f52b</h1>
    <p class="subtitle">Enter your name to start playing!</p>
    <form class="name-form" action="/api/play" method="get">
      <input class="name-input" type="text" name="name"
             placeholder="Your name..." required autofocus maxlength="20" />
      <button class="btn-primary" type="submit">&#x25B6;&nbsp; Start Game</button>
    </form>
    <footer>Snake beats Water &bull; Water beats Gun &bull; Gun beats Snake</footer>"""
    return page(body)


def choice_screen(name, wins, losses, ties):
    rounds = wins + losses + ties
    params = urlencode({"wins": wins, "losses": losses, "ties": ties})
    body = f"""
    <h1>\U0001f40d Snake Water Gun \U0001f52b</h1>
    <div class="player-row">
      <span class="player-tag">Hello, <strong>{escape(name)}</strong>! \U0001f44b</span>
      <a class="btn-new-player" href="/api/play?new_player=1">&#x21BA; New Player</a>
    </div>
    <div class="scoreboard">
      <div class="score-box score-rnd"><div class="score-val">{rounds}</div><div class="score-lbl">Rounds</div></div>
      <div class="score-box score-win"><div class="score-val">{wins}</div><div class="score-lbl">Wins</div></div>
      <div class="score-box score-lose"><div class="score-val">{losses}</div><div class="score-lbl">Losses</div></div>
      <div class="score-box score-tie"><div class="score-val">{ties}</div><div class="score-lbl">Ties</div></div>
    </div>
    <p class="subtitle">Make your choice:</p>
    <form class="choices" action="/api/play" method="get">
      <input type="hidden" name="wins" value="{wins}" />
      <input type="hidden" name="losses" value="{losses}" />
      <input type="hidden" name="ties" value="{ties}" />
      <button class="btn" name="choice" value="S">\U0001f40d<span class="lbl">Snake</span></button>
      <button class="btn" name="choice" value="W">\U0001f4a7<span class="lbl">Water</span></button>
      <button class="btn" name="choice" value="G">\U0001f52b<span class="lbl">Gun</span></button>
    </form>
    <div class="actions">
      <a class="btn-sm btn-end" href="/api/play?{params}&end=1">\U0001f3c1 End Game</a>
    </div>
    <footer>Snake beats Water &bull; Water beats Gun &bull; Gun beats Snake</footer>"""
    return page(body)


def result_screen(name, user, comp, outcome, label, color, reason, wins, losses, ties):
    rounds   = wins + losses + ties
    next_url = "/api/play?" + urlencode({"wins": wins, "losses": losses, "ties": ties})
    end_url  = "/api/play?" + urlencode({"wins": wins, "losses": losses, "ties": ties, "end": 1})
    head_extra = f"""
    <script>
      var timer = setTimeout(function() {{ window.location.href = "{next_url}"; }}, 2000);
      function cancel() {{ clearTimeout(timer); }}
    </script>"""
    body = f"""
    <h1>\U0001f40d Snake Water Gun \U0001f52b</h1>
    <div class="player-row">
      <span class="player-tag">Round <strong>{rounds}</strong> &mdash; <strong style="color:#e94560">{escape(name)}</strong></span>
      <a class="btn-new-player" href="/api/play?new_player=1" onclick="cancel()">&#x21BA; New Player</a>
    </div>
    <div class="scoreboard">
      <div class="score-box score-rnd"><div class="score-val">{rounds}</div><div class="score-lbl">Rounds</div></div>
      <div class="score-box score-win"><div class="score-val">{wins}</div><div class="score-lbl">Wins</div></div>
      <div class="score-box score-lose"><div class="score-val">{losses}</div><div class="score-lbl">Losses</div></div>
      <div class="score-box score-tie"><div class="score-val">{ties}</div><div class="score-lbl">Ties</div></div>
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
      <div class="countdown-txt">Next round in 2 seconds...</div>
    </div>
    <div class="actions">
      <a class="btn-sm" href="{next_url}" onclick="cancel()">\U0001f504 Play Now</a>
      <a class="btn-sm btn-end" href="{end_url}" onclick="cancel()">\U0001f3c1 End Game</a>
    </div>
    <footer>Snake beats Water &bull; Water beats Gun &bull; Gun beats Snake</footer>"""
    return page(body, head_extra, f"Round {rounds} - {name}")


def final_screen(name, wins, losses, ties):
    rounds = wins + losses + ties
    if rounds == 0:
        verdict, vcolor = "No rounds played!", "#888"
    elif wins > losses:
        verdict, vcolor = f"\U0001f3c6 {escape(name)} wins! Great job!", "#4caf50"
    elif losses > wins:
        verdict, vcolor = "\U0001f916 Computer wins! Better luck next time!", "#e94560"
    else:
        verdict, vcolor = "\U0001f91d It's a draw!", "#f0c040"
    win_pct = round(wins / rounds * 100) if rounds else 0
    body = f"""
    <h1>\U0001f3c1 Game Over!</h1>
    <p class="subtitle" style="color:#f0c040;font-size:1rem;margin-bottom:1.2rem;">{escape(name)}'s Final Score</p>
    <div class="final-grid">
      <div class="final-box"><div class="fval" style="color:#64b5f6">{rounds}</div><div class="flbl">Rounds</div></div>
      <div class="final-box"><div class="fval" style="color:#4caf50">{wins}</div><div class="flbl">Wins</div></div>
      <div class="final-box"><div class="fval" style="color:#e94560">{losses}</div><div class="flbl">Losses</div></div>
      <div class="final-box"><div class="fval" style="color:#f0c040">{ties}</div><div class="flbl">Ties</div></div>
      <div class="final-box"><div class="fval" style="color:#ab47bc">{win_pct}%</div><div class="flbl">Win Rate</div></div>
    </div>
    <div class="verdict" style="color:{vcolor}">{verdict}</div>
    <a class="new-game-btn" href="/api/play">\U0001f504 Play Again</a><br/>
    <a class="new-player-btn" href="/api/play?new_player=1">&#x21BA; Switch Player</a>
    <footer style="margin-top:1.5rem">Snake beats Water &bull; Water beats Gun &bull; Gun beats Snake</footer>"""
    return page(body, title=f"Final Score - {name}")

# ---------------------------------------------------------------------------
# Handler
# ---------------------------------------------------------------------------

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path   = parsed.path
        qs     = parse_qs(parsed.query)
        g      = lambda k, d="": qs.get(k, [d])[0]

        # --- Static PWA assets ---
        if path == "/manifest.json":
            self._send(200, MANIFEST, "application/manifest+json", cache=True)
            return
        if path == "/sw.js":
            self._send(200, SW_JS, "application/javascript", cache=False)
            return
        if path == "/icon-192.png":
            self._send(200, ICON_192, "image/png", cache=True)
            return
        if path == "/icon-512.png":
            self._send(200, ICON_512, "image/png", cache=True)
            return

        # --- Game ---
        extra_headers = []
        new_player = g("new_player")
        name_param = g("name").strip()
        choice     = g("choice").strip().upper()
        end        = g("end")
        wins       = int(g("wins",   "0"))
        losses     = int(g("losses", "0"))
        ties       = int(g("ties",   "0"))

        if new_player:
            extra_headers.append(("Set-Cookie", clear_cookie_header()))
            html = name_screen()
        elif name_param:
            extra_headers.append(("Set-Cookie", set_cookie_header(name_param)))
            self._send(302, None, None, extra_headers + [("Location", "/api/play")])
            return
        else:
            name = read_cookie_name(self.headers)
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

        self._send(200, html.encode(), "text/html; charset=utf-8", extra_headers)

    def _send(self, status, body, content_type, extra_headers=None, cache=False):
        self.send_response(status)
        if content_type:
            self.send_header("Content-Type", content_type)
        if cache:
            self.send_header("Cache-Control", "public, max-age=86400")
        for k, v in (extra_headers or []):
            self.send_header(k, v)
        self.end_headers()
        if body:
            self.wfile.write(body if isinstance(body, bytes) else body.encode())
