import os

_placeholders = {"dev-only-change-me", "", "change-me"}


class Config:
    QNA_DIR = os.environ.get("CODY_QNA_DIR", "qna")
    SECRET_KEY = os.environ.get("CODY_SECRET_KEY", "dev-only-change-me")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False

    def __init__(self):
        super().__init__()
        if self.SECRET_KEY in _placeholders:
            raise ValueError(
                "CODY_SECRET_KEY must be set to a secure value in production. "
                "Generate one with: python -c 'import secrets; print(secrets.token_hex(32))'"
            )
