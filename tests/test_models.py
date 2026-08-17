import pytest

import config
from models import categoria as categoria_model
from models import receta as receta_model
from models.database import init_db


@pytest.fixture
def db_path(tmp_path):
    path = str(tmp_path / "test_recetas.db")
    init_db(db_path=path, schema_path=config.SCHEMA_PATH)
    return path


def test_crear_y_listar_categoria(db_path):
    categoria_model.create("Postres", db_path=db_path)

    categorias = categoria_model.get_all(db_path=db_path)

    assert len(categorias) == 1
    assert categorias[0]["nombre"] == "Postres"


def test_obtener_categoria_por_id(db_path):
    categoria_id = categoria_model.create("Sopas", db_path=db_path)

    categoria = categoria_model.get_by_id(categoria_id, db_path=db_path)

    assert categoria["nombre"] == "Sopas"


def test_crear_y_obtener_receta(db_path):
    categoria_id = categoria_model.create("Postres", db_path=db_path)
    receta_id = receta_model.create(
        {
            "nombre": "Flan",
            "descripcion": "Postre clásico",
            "ingredientes": "Huevos\nLeche\nAzúcar",
            "pasos": "Mezclar\nHornear",
            "tiempo_preparacion": 60,
            "porciones": 4,
            "categoria_id": categoria_id,
        },
        db_path=db_path,
    )

    receta = receta_model.get_by_id(receta_id, db_path=db_path)

    assert receta["nombre"] == "Flan"
    assert receta["categoria_nombre"] == "Postres"
    assert receta["tiempo_preparacion"] == 60


def test_listar_recetas_con_filtros(db_path):
    postres_id = categoria_model.create("Postres", db_path=db_path)
    categoria_model.create("Sopas", db_path=db_path)
    receta_model.create(
        {
            "nombre": "Flan",
            "descripcion": None,
            "ingredientes": "Huevos",
            "pasos": "Mezclar",
            "tiempo_preparacion": None,
            "porciones": None,
            "categoria_id": postres_id,
        },
        db_path=db_path,
    )
    receta_model.create(
        {
            "nombre": "Sopa de tomate",
            "descripcion": None,
            "ingredientes": "Tomate",
            "pasos": "Cocinar",
            "tiempo_preparacion": None,
            "porciones": None,
            "categoria_id": None,
        },
        db_path=db_path,
    )

    resultado_nombre = receta_model.get_all(nombre="Flan", db_path=db_path)
    resultado_categoria = receta_model.get_all(categoria_id=postres_id, db_path=db_path)

    assert len(resultado_nombre) == 1
    assert resultado_nombre[0]["nombre"] == "Flan"
    assert len(resultado_categoria) == 1
    assert resultado_categoria[0]["nombre"] == "Flan"


def test_actualizar_y_eliminar_receta(db_path):
    receta_id = receta_model.create(
        {
            "nombre": "Sopa",
            "descripcion": None,
            "ingredientes": "Agua",
            "pasos": "Hervir",
            "tiempo_preparacion": 10,
            "porciones": 2,
            "categoria_id": None,
        },
        db_path=db_path,
    )

    receta_model.update(
        receta_id,
        {
            "nombre": "Sopa actualizada",
            "descripcion": None,
            "ingredientes": "Agua\nSal",
            "pasos": "Hervir\nServir",
            "tiempo_preparacion": 15,
            "porciones": 3,
            "categoria_id": None,
        },
        db_path=db_path,
    )
    receta_actualizada = receta_model.get_by_id(receta_id, db_path=db_path)
    assert receta_actualizada["nombre"] == "Sopa actualizada"
    assert receta_actualizada["porciones"] == 3

    receta_model.delete(receta_id, db_path=db_path)
    assert receta_model.get_by_id(receta_id, db_path=db_path) is None
