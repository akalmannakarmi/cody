import json
import os

from flask import (
    Blueprint,
    abort,
    current_app,
    redirect,
    render_template,
    request,
    send_from_directory,
)

from . import limiter
from .data import IMAGE_EXTENSIONS, QnaStore
from .utils import resolve_safe_image_path

main_bp = Blueprint("main", __name__)
play_bp = Blueprint("play", __name__)
images_bp = Blueprint("images", __name__)


def get_store():
    return QnaStore(current_app.config["QNA_DIR"])


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/versions")
def versions():
    store = get_store()
    return render_template("versions.html", versions=store.versions())


@main_bp.route("/contact")
def contact():
    return render_template("contact.html")


@play_bp.route("/play")
def play():
    version = request.args.get("ver")
    if not version:
        return redirect("/play?ver=all")

    store = get_store()
    available = store.versions()
    if version not in available:
        abort(404)

    categories = store.categories(version)
    values = sorted(
        {v for category in categories for v in store.values(version, category)}
    )
    board = {
        "version": version,
        "categories": categories,
        "values": values,
    }
    return render_template(
        "play.html",
        current_version=version,
        categories=categories,
        board=board,
    )


@images_bp.route("/getImg/<path:path>", methods=["GET"])
def serve_image(path):
    full = resolve_safe_image_path(current_app.config["QNA_DIR"], path)
    if full is None:
        abort(404)
    if os.path.splitext(full)[1].lower() not in IMAGE_EXTENSIONS:
        abort(404)
    root = os.path.realpath(current_app.config["QNA_DIR"])
    relative = os.path.relpath(full, root)
    return send_from_directory(root, relative)


@images_bp.route("/qna", methods=["POST"])
@limiter.limit("30/minute")
def qna():
    store = get_store()
    try:
        payload = json.loads(request.data or b"{}")
    except (ValueError, TypeError):
        return _qna_error("Request body is not valid JSON"), 400

    if not all(key in payload for key in ("version", "category", "value")):
        return _qna_error("Missing version, category or value"), 400

    version = payload["version"]
    category = payload["category"]

    if version not in store.versions():
        return _qna_error(f"Unknown version: {version}"), 404
    if category not in store.categories(version):
        return _qna_error(f"Unknown category: {category}"), 404

    try:
        value = int(payload["value"])
    except (ValueError, TypeError):
        return _qna_error("Value must be an integer"), 400

    question = store.random_question(version, category, value)
    if question is None:
        return _qna_error("No usable question found"), 400

    response = {
        "category": category,
        "value": value,
        "question": {
            "text": question["text"],
            "code": question["code"],
            "image": question["image"],
        },
        "answer": question["answer"],
    }
    return response, 200


def _qna_error(message):
    return {"error": message}
