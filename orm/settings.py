from tortoise import Tortoise

import sys

sys.path.append("../")


DB_NAME = "cacha_db"
DB_USERNAME = "cache_holder"
DB_PASSWORD = "abobus"
DB_IP = "127.0.0.1"
DB_PORT = "5432"


DB_URL = f"postgres://{DB_USERNAME}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}"


TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                "auth.models",
            ],
            "default_connection": "default",
            "maxsize": 50
        },
    },
}


async def init():
    """Call anywhere when you need to init base
       in the scripts or whatever
    """
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": TORTOISE_ORM["apps"]["models"]["models"]}
    )
    await Tortoise.generate_schemas()


BLUEPRINTS = {
    "auth_bp": "sanic_auth_bp"
}

API_CODES = {
    4000: "ok",
    4001: "error",
    4002: "no_access"
}

TOKEN_LIFESPAN = 14