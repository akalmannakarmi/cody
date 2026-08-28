import os

_placeholders: set[str] = {"dev-only-change-me", "", "change-me"}


class Config:
    QNA_DIR: str = os.environ.get("CODY_QNA_DIR", "qna")
    SECRET_KEY: str = os.environ.get("CODY_SECRET_KEY", "dev-only-change-me")
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "Lax"


class DevConfig(Config):
    DEBUG: bool = True


class ProdConfig(Config):
    DEBUG: bool = False

    def __init__(self) -> None:
        super().__init__()
        if self.SECRET_KEY in _placeholders:
            raise ValueError(
                "CODY_SECRET_KEY must be set to a secure value in production. "
                "Generate one with: python -c 'import secrets; print(secrets.token_hex(32))'"
            )
