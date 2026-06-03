# Snake Water Gun Game

A simple Python game implementing the classic Snake-Water-Gun rules.

Rules
- Snake drinks Water (Snake wins)
- Water douses Gun (Water wins)
- Gun kills Snake (Gun wins)

Terminal Usage

Run the game from the terminal:

```bash
python snakeWaterGunGame.py
```

Input choices
- `S` - Snake
- `W` - Water
- `G` - Gun

Browser Usage

The browser version submits the player's choice to a Python Vercel function at `/api/play`.

Local Browser Usage

Run the local Python web server:

```bash
python server.py
```

Then open:

```text
http://127.0.0.1:8000
```

Example

```text
Enter your choice (Snake: S, Water: W, Gun: G): S
You chose Snake. Computer chose Water. You win!
```

Notes
- This is a single-round game for both terminal and browser use.

Contributing
- Feel free to open issues or submit pull requests to improve the game.
