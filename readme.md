# Cody

A Jeopardy-style coding quiz (Flask + Bootstrap). Pick a tile → reveal a question → flip to the answer.

## Tech stack

- **Flask** web app
- **uv**-managed Python project
- **Bootstrap 5** (CDN)
- **pytest** for tests

## Quickstart

```bash
uv sync
uv run flask run
```

Then open <http://localhost:5000>.

## How to play

1. Go to **Versions** and pick a board (e.g. `ver1` or `all`).
2. Click a tile (value) under any category.
3. The question modal opens — reveal text, code, or image.
4. Click **Answer** to flip to the answer modal.
5. Click **Reset board** to re-enable the tiles.

## Adding questions

Question data lives as JSON in `qna/<version>/<category>/<value>.json` like:

```json
{ "qnas": [ { "question": "…", "answer": "…" } ] }
```

Each item uses these (legacy) keys: `question`/`answer` (text),
`cquestion`/`canswer` (code), `qimage`/`aimage` (image path). Use the CLI to add one:

```bash
uv run python scripts/create_qna.py --help
uv run python scripts/create_qna.py --version ver1 --category Memes --value 20 \
    --text "What is…?" --answer "It is…"
```

Validate your data with:

```bash
uv run python scripts/validate_qna.py
```

See [docs/usage.md](docs/usage.md), [CONTRIBUTING.md](CONTRIBUTING.md), and [CHANGELOG.md](CHANGELOG.md).
