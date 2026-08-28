import os

from app import create_app
from app.config import DevConfig, ProdConfig

config = ProdConfig if os.environ.get("CODY_ENV") == "production" else DevConfig

app = create_app(config)

if __name__ == "__main__":
    app.run(debug=False)
