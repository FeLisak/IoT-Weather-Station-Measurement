CREATE TABLE IF NOT EXISTS leituras (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  temperatura_externa REAL NOT NULL,
  umidade_do_solo REAL NOT NULL,
  timestamp DATETIME DEFAULT (datetime('now','localtime'))
);