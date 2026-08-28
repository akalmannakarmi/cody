# Cody Usage Guide

## What is Cody?

Cody is a Jeopardy-style coding quiz. A quizmaster (or a single user) picks a board
from the Versions page, clicks tiles to reveal computer-science questions, and flips
to the answers. It is designed for classrooms, study groups, and casual quiz nights.

## Navigating the site

- **Home** (`/`)  overview of the game and its rules.
- **Versions** (`/versions`)  lists available boards (e.g. `ver1`, `all`).
- **Play** (`/play?ver=<version>`)  the game board.

## Playing a round

1. Pick a board from the Versions page. Each board groups categories and values.
2. Click a tile to reveal its question. The modal shows text, code, or an image
   depending on how the question was authored.
3. Read the question aloud (or silently), then click **Answer** to reveal the answer.
4. After all tiles are used, click **Reset board** to re-enable every tile without
   reloading the page.

## Categories and values

Each board has categories (columns) and point values (rows). Higher values
correspond to harder questions. Not every category/value combination is guaranteed
to have a question  an empty tile shows the API error instead of a question.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Tile shows "error" on click | The JSON file is missing or empty | Add a valid JSON file at `qna/<ver>/<cat>/<value>.json` |
| Image not loading | Wrong path in `qimage`/`aimage` | Check the image path relative to the repo root |
| Port 5000 already in use | Another process is on that port | Kill the other process or use `flask run -p 5001` |
| `404` on `/versions` | Template missing | Ensure `app/templates/versions.html` exists |

## Deployment

```bash
docker compose up -d --build
```

The app is served on port 5000. Set `CODY_SECRET_KEY` in production.

```bash
CODY_SECRET_KEY=your-secret-here docker compose up -d --build
```
