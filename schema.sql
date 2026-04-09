CREATE TABLE IF NOT EXISTS leituras (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  temperatura_externa REAL NOT NULL,
  umidade_do_solo REAL NOT NULL,
  timestamp DATETIME DEFAULT (datetime('now','localtime'))
);

-- Dados de exemplo para testes (30 leituras com variações realistas)
INSERT OR IGNORE INTO leituras (id, temperatura_externa, umidade_do_solo, timestamp) VALUES
  (1,  22.5, 450, datetime('now', '-34 days')),
  (2,  23.1, 480, datetime('now', '-34 days', '+2 hours')),
  (3,  21.8, 420, datetime('now', '-34 days', '+4 hours')),
  (4,  20.5, 350, datetime('now', '-34 days', '+6 hours')),
  (5,  19.2, 380, datetime('now', '-34 days', '+8 hours')),
  (6,  18.5, 360, datetime('now', '-34 days', '+10 hours')),
  (7,  19.8, 390, datetime('now', '-34 days', '+12 hours')),
  (8,  21.3, 440, datetime('now', '-34 days', '+14 hours')),
  (9,  23.5, 500, datetime('now', '-34 days', '+16 hours')),
  (10, 24.2, 520, datetime('now', '-34 days', '+18 hours')),
  (11, 21.0, 430, datetime('now', '-20 days')),
  (12, 22.2, 470, datetime('now', '-20 days', '+3 hours')),
  (13, 23.5, 500, datetime('now', '-20 days', '+6 hours')),
  (14, 24.1, 530, datetime('now', '-20 days', '+9 hours')),
  (15, 23.9, 515, datetime('now', '-20 days', '+12 hours')),
  (16, 22.5, 480, datetime('now', '-20 days', '+15 hours')),
  (17, 20.8, 410, datetime('now', '-20 days', '+18 hours')),
  (18, 19.5, 370, datetime('now', '-20 days', '+21 hours')),
  (19, 20.2, 385, datetime('now', '-10 days')),
  (20, 21.8, 430, datetime('now', '-10 days', '+4 hours')),
  (21, 23.2, 480, datetime('now', '-10 days', '+8 hours')),
  (22, 24.5, 540, datetime('now', '-10 days', '+12 hours')),
  (23, 25.1, 560, datetime('now', '-10 days', '+16 hours')),
  (24, 24.0, 525, datetime('now', '-10 days', '+20 hours')),
  (25, 22.3, 470, datetime('now', '-5 days')),
  (26, 21.5, 440, datetime('now', '-5 days', '+5 hours')),
  (27, 22.8, 475, datetime('now', '-5 days', '+10 hours')),
  (28, 23.9, 515, datetime('now', '-5 days', '+15 hours')),
  (29, 22.0, 450, datetime('now', '-1 days')),
  (30, 23.6, 510, datetime('now', '-1 days', '+8 hours'));