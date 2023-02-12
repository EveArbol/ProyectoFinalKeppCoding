DROP TABLE IF EXISTS posts;

CREATE TABLE movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date Text NOT NULL,
    time Text NOT NULL,
    moneda_from TEXT NOT NULL,
    cantidad_from Real NOT NULL,
    moneda_to TEXT NOT NULL,
    cantidad_to Real NOT NULL
);