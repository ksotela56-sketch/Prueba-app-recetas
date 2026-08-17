from models.database import get_connection


def get_all(db_path=None):
    conn = get_connection(db_path)
    filas = conn.execute("SELECT * FROM categorias ORDER BY nombre").fetchall()
    conn.close()
    return filas


def get_by_id(categoria_id, db_path=None):
    conn = get_connection(db_path)
    fila = conn.execute(
        "SELECT * FROM categorias WHERE id = ?", (categoria_id,)
    ).fetchone()
    conn.close()
    return fila


def create(nombre, db_path=None):
    conn = get_connection(db_path)
    cursor = conn.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return nuevo_id
