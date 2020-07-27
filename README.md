# Pong

This is a remake of the classic game [Pong](https://en.wikipedia.org/wiki/Pong).

## Getting started

Set up a virtual environment, for example:

```bash
$ python3 -m venv .venv
```

Activate the virtual environment:

```bash
$ source .venv/bin/activate
```

Install the requirements:

```bash
$ pip install wheel
$ pip install -r requirements.txt
```

Run the game:

```bash
python3 main.py [game_mode]
```

### Game Mode

There are four modes to run the game:

- 0: Both paddles are controlled by AI.
- 1: The left paddle is controlled by keys 'w' (up) and 's' (down) and the right paddle
  is controlled by an AI.
- 2: The left paddle is controlled by an AI and the right paddle is controlled by keys
  up arrow and down arrow.
- 3: The left paddle is controlled by keys 'w' (up) and 's' (down) and the right paddle
  is controlled by keys up arrow and down arrow.

By default, the game is executed with `game_mode = 1`.

## Credits

- Sound effects made with [bfxr](https://www.bfxr.net/).
- Font from [https://www.1001fonts.com/joystix-font.html](https://www.1001fonts.com/joystix-font.html)
