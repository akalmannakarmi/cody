# Contributing to Cody

Thanks for your interest in contributing! Cody is a small project — keep it simple.

## Setup

```bash
git clone git@github.com:akalmannakarmi/cody.git
cd cody
uv sync
```

## Running the app

```bash
uv run flask run
```

Open <http://localhost:5000>.

## Running tests

```bash
uv run pytest
```

All tests must pass before submitting a change.

## Validating question data

After editing any JSON under `qna/`:

```bash
uv run python scripts/validate_qna.py
```

Fix any errors before committing.

## Code style

- Python stdlib is preferred, avoid adding dependencies unless necessary.
- No comments unless specifically asked for.
- Follow existing conventions in the file you are editing.
- Keep things simple and readable.

## Adding a new version or category

1. Create the directory structure: `qna/<version>/<category>/`.
2. Add JSON files named `<value>.json` (value is an integer, e.g. `100.json`).
3. Validate with the validator script.
4. The board auto-discovers versions, categories, and values on load.

## Commit messages

- Going forward use conventional commits: `type(scope): summary`
  - e.g. `feat(data): add image validation to QnaStore`
  - e.g. `fix(routes): handle missing version param`

## Proposing changes

1. Fork the repo or create a branch from `main`.
2. Make your changes and ensure `uv run pytest` passes.
3. Open a pull request with a clear description of what changed and why.

## Questions?

Open an issue on the [GitHub repo](https://github.com/akalmannakarmi/cody) or
email akalnakarmi1@gmail.com.
