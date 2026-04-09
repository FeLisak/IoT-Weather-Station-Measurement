import sqlite3
from config import DB_PATH, SCHEMA_PATH


def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=5000')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        with open(SCHEMA_PATH, 'r') as f:
            conn.executescript(f.read())


def inserir_leitura(temperatura_externa, umidade_do_solo):
    with get_db_connection() as conn:
        cursor = conn.execute(
            'INSERT INTO leituras (temperatura_externa, umidade_do_solo) VALUES (?, ?)',
            (temperatura_externa, umidade_do_solo)
        )
        return cursor.lastrowid


def listar_leituras(limite=50):
    with get_db_connection() as conn:
        rows = conn.execute(
            'SELECT * FROM leituras ORDER BY timestamp DESC LIMIT ?',
            (limite,)
        ).fetchall()
        return [dict(row) for row in rows]


def buscar_leitura(id):
    with get_db_connection() as conn:
        row = conn.execute(
            'SELECT * FROM leituras WHERE id = ?',
            (id,)
        ).fetchone()
        return dict(row) if row else None


def atualizar_leitura(id, dados):
    campos_permitidos = {'temperatura_externa', 'umidade_do_solo'}
    campos = {k: v for k, v in dados.items() if k in campos_permitidos}
    if not campos:
        raise ValueError('Nenhum campo válido para atualizar')
    set_clause = ', '.join(f'{k} = ?' for k in campos)
    valores = list(campos.values()) + [id]
    with get_db_connection() as conn:
        cursor = conn.execute(
            f'UPDATE leituras SET {set_clause} WHERE id = ?',
            valores
        )
        return cursor.rowcount > 0


def deletar_leitura(id):
    with get_db_connection() as conn:
        cursor = conn.execute(
            'DELETE FROM leituras WHERE id = ?',
            (id,)
        )
        return cursor.rowcount > 0
