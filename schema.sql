-- Esquema de la base de datos de la app de recetas

CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS recetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    ingredientes TEXT NOT NULL,
    pasos TEXT NOT NULL,
    tiempo_preparacion INTEGER,
    porciones INTEGER,
    categoria_id INTEGER,
    fecha_creacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias (id) ON DELETE SET NULL
);
