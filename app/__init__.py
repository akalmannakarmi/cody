import logging
import os

from flask import Flask, render_template

from .config import DevConfig
from .routes import images_bp, main_bp, play_bp


def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or DevConfig)
    app.config["QNA_DIR"] = os.path.abspath(app.config["QNA_DIR"])

    app.register_blueprint(main_bp)
    app.register_blueprint(play_bp)
    app.register_blueprint(images_bp)

    app.register_error_handler(404, _handle_404)
    app.register_error_handler(500, _handle_500)

    _configure_logging(app)

    return app


def _handle_404(error):
    return render_template("404.html"), 404


def _handle_500(error):
    current_app_logger = logging.getLogger(__name__)
    current_app_logger.exception("Unhandled error: %s", error)
    return render_template("error.html"), 500


def _configure_logging(app):
    level = logging.DEBUG if app.debug else logging.INFO
    logging.basicConfig(level=level)
    app.logger.setLevel(level)
