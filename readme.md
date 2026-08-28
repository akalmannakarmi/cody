# Cody

A Jeopardy-style coding quiz built with Flask. Pick a tile, reveal a computer-science
question, and flip to the answer. No accounts, no scoring engine  just a reveal board
for classrooms, quiz nights, or self-study.

## Tech stack

- **Flask**  Python web framework
- **uv**  Python package manager (lockfile + virtual env)
- **Bootstrap 5**  CSS/JS from jsDelivr CDN
- **pytest**  test suite
- **Docker**  optional containerised deployment

## Quickstart

```bash
uv sync
uv run flask run
```

Open <http://localhost:5000>.

### Docker

```bash
docker compose up -d --build
```

The app is served on port 5000.

## How to play

1. Go to **Versions** and pick a board (`ver1`, `all`, etc.).
2. Click a tile (point value) under any category.
3. A question modal opens  it may contain text, a code block, or an image.
4. Click **Answer** to flip to the answer modal.
5. Click **Reset board** to re-enable all tiles for another round.

Higher values correspond to harder questions. The board resets in-place without a
page reload.

## Project layout

```
cody/
├── main.py              # thin entry point
├── pyproject.toml       # uv-managed project metadata + deps
├── app/
│   ├── __init__.py      # create_app() factory
│   ├── config.py        # Config / DevConfig / ProdConfig
│   ├── routes.py        # main_bp, play_bp, images_bp blueprints
│   ├── data.py          # QnaStore: discovery, load, normalize, cache
│   ├── static/          # css/, js/, img/
│   └── templates/       # Jinja2 templates (base, nav, play, …)
├── qna/                 # JSON question data (legacy on-disk format)
├── scripts/
│   ├── create_qna.py    # CLI to append a question
│   └── validate_qna.py  # CLI data validator
├── tests/               # pytest suite
├── Dockerfile           # uv multi-stage build
└── docker-compose.yml
```

## Adding questions

Question data lives as JSON files at `qna/<version>/<category>/<value>.json`.
Each file contains a `qnas` array:

```json
{
  "qnas": [
    {
      "question": "What does CPU stand for?",
      "answer": "Central Processing Unit"
    }
  ]
}
```

Supported legacy keys per QnA item:

| Key | Purpose |
|---|---|
| `question` / `answer` | Plain text |
| `cquestion` / `canswer` | Code block |
| `qimage` / `aimage` | Image path (relative to repo root) |

### Using the CLI

```bash
uv run python scripts/create_qna.py \
    --version ver1 --category "Computer Basics" --value 100 \
    --text "What does CPU stand for?" \
    --answer "Central Processing Unit"
```

Run `uv run python scripts/create_qna.py --help` for all options.

### Validating data

```bash
uv run python scripts/validate_qna.py
```

Reports errors (broken JSON, missing images) and warnings (legacy-only keys).
Fix flagged issues before committing.

## Tests

```bash
uv run pytest
```

Tests live in `tests/` and cover routes, the data layer, and the CLI scripts.

## Deployment

### Docker Compose

```bash
docker compose up -d --build
```

The app listens on `0.0.0.0:5000`. Set the `CODY_SECRET_KEY` environment variable
in production.

### Environment variables

| Variable | Default | Description |
|---|---|---|
| `CODY_SECRET_KEY` | `dev-only-change-me` | Flask secret key |
| `CODY_QNA_DIR` | `qna` | Path to question data directory |
| `CODY_ENV` |  | Set to `production` for ProdConfig |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
