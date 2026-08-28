import os


class Config:
    SECRET_KEY = os.environ.get("CODY_SECRET_KEY", "dev-only-change-me")
    QNA_DIR = os.environ.get("CODY_QNA_DIR", "qna")


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False
