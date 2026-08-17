import pytest

import config
from app import create_app
from models.database import init_db


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test_recetas.db")
    monkeypatch.setattr(config, "DATABASE_PATH", db_path)
    init_db(db_path=db_path, schema_path=config.SCHEMA_PATH)

    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_listado_vacio(client):
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert "No se encontraron recetas".encode() in respuesta.data


def test_crear_categoria(client):
    respuesta = client.post("/categorias/nueva", data={"nombre": "Postres"}, follow_redirects=True)
    assert respuesta.status_code == 200
    assert "Postres".encode() in respuesta.data


def test_crear_receta_y_verla_en_listado(client):
    respuesta = client.post(
        "/recetas/nueva",
        data={
            "nombre": "Flan",
            "descripcion": "Postre clásico",
            "ingredientes": "Huevos\nLeche",
            "pasos": "Mezclar\nHornear",
            "tiempo_preparacion": "60",
            "porciones": "4",
            "categoria_id": "",
        },
        follow_redirects=True,
    )
    assert respuesta.status_code == 200
    assert "Flan".encode() in respuesta.data

    listado = client.get("/")
    assert "Flan".encode() in listado.data


def test_crear_receta_sin_nombre_falla(client):
    respuesta = client.post(
        "/recetas/nueva",
        data={
            "nombre": "",
            "ingredientes": "Huevos",
            "pasos": "Mezclar",
        },
        follow_redirects=True,
    )
    assert respuesta.status_code == 200
    assert "El nombre es obligatorio".encode() in respuesta.data


def test_editar_y_eliminar_receta(client):
    client.post(
        "/recetas/nueva",
        data={
            "nombre": "Sopa",
            "ingredientes": "Agua",
            "pasos": "Hervir",
        },
        follow_redirects=True,
    )
    listado = client.get("/")
    receta_id = 1

    respuesta_editar = client.post(
        f"/recetas/{receta_id}/editar",
        data={
            "nombre": "Sopa actualizada",
            "ingredientes": "Agua\nSal",
            "pasos": "Hervir\nServir",
        },
        follow_redirects=True,
    )
    assert "Sopa actualizada".encode() in respuesta_editar.data

    respuesta_eliminar = client.post(f"/recetas/{receta_id}/eliminar", follow_redirects=True)
    assert respuesta_eliminar.status_code == 200
    assert "Receta eliminada correctamente".encode() in respuesta_eliminar.data
