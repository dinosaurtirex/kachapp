from sanic import Sanic

from auth.auth_bp import auth_bp
from orm.settings import DB_URL, TORTOISE_ORM
from tortoise.contrib.sanic import register_tortoise


app = Sanic("stats-service")
app.config.OAS = False


# Auth application 
app.blueprint(auth_bp)


register_tortoise(
    app,
    db_url=DB_URL,
    modules={
        "models": TORTOISE_ORM["apps"]["models"]["models"]
    },
    generate_schemas=True
)


if __name__ == "__main__":
    app.run(host="127.0.0.2", port=500, dev=True)