CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT NOT NULL UNIQUE,
    contraseña TEXT NOT NULL,
    codigo_recuperacion TEXT NOT NULL
);