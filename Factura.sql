CREATE TABLE IF NOT EXISTS Factura (
    id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    empresa TEXT NOT NULL,
    fecha TEXT NOT NULL,
    productos TEXT NOT NULL,
    total REAL NOT NULL,
    forma_pago TEXT NOT NULL
);
