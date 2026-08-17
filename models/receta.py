from models.database import get_connection

_SELECT_BASE = """
    SELECT recetas.*, categorias.nombre AS categoria_nombre
    FROM recetas
    LEFT JOIN categorias ON categorias.id = recetas.categoria_id
"""


def get_all(nombre=None, categoria_id=None, db_path=None):
    conn = get_connection(db_path)
    condiciones = []
    parametros = []

    if nombre:
        condiciones.append("recetas.nombre LIKE ?")
        parametros.append(f"%{nombre}%")
    if categoria_id:
        condiciones.append("recetas.categoria_id = ?")
        parametros.append(categoria_id)

    query = _SELECT_BASE
    if condiciones:
        query += " WHERE " + " AND ".join(condiciones)
    query += " ORDER BY recetas.fecha_creacion DESC"

    filas = conn.execute(query, parametros).fetchall()
    conn.close()
    return filas


def get_by_id(receta_id, db_path=None):
    conn = get_connection(db_path)
    fila = conn.execute(
        _SELECT_BASE + " WHERE recetas.id = ?", (receta_id,)
    ).fetchone()
    conn.close()
    return fila


def create(datos, db_path=None):
    conn = get_connection(db_path)
    cursor = conn.execute(
        """
        INSERT INTO recetas
            (nombre, descripcion, ingredientes, pasos, tiempo_preparacion, porciones, categoria_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datos["nombre"],
            datos.get("descripcion"),
            datos["ingredientes"],
            datos["pasos"],
            datos.get("tiempo_preparacion"),
            datos.get("porciones"),
            datos.get("categoria_id"),
        ),
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return nuevo_id


def update(receta_id, datos, db_path=None):
    conn = get_connection(db_path)
    conn.execute(
        """
        UPDATE recetas
        SET nombre = ?, descripcion = ?, ingredientes = ?, pasos = ?,
            tiempo_preparacion = ?, porciones = ?, categoria_id = ?
        WHERE id = ?
        """,
        (
            datos["nombre"],
            datos.get("descripcion"),
            datos["ingredientes"],
            datos["pasos"],
            datos.get("tiempo_preparacion"),
            datos.get("porciones"),
            datos.get("categoria_id"),
            receta_id,
        ),
    )
    conn.commit()
    conn.close()


def delete(receta_id, db_path=None):
    conn = get_connection(db_path)
    conn.execute("DELETE FROM recetas WHERE id = ?", (receta_id,))
    conn.commit()
    conn.close()
