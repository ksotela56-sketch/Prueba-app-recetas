import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY", "clave-de-desarrollo-cambiar-en-produccion")
DATABASE_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "recetas.db"))
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")
