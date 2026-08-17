import os

from flask import Flask

import config
from controllers.categoria_controller import categorias_bp
from controllers.receta_controller import recetas_bp
from models.database import init_db


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join("views", "templates"),
        static_folder=os.path.join("views", "static"),
    )
    app.config["SECRET_KEY"] = config.SECRET_KEY

    if not os.path.exists(config.DATABASE_PATH):
        init_db()

    app.register_blueprint(recetas_bp)
    app.register_blueprint(categorias_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
