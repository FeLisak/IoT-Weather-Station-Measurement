"""
Arquivo de configuração central para a Estação Meteorológica IoT.
Centraliza variáveis de ambiente e constantes do projeto.
"""

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

# ── Configuração de Banco de Dados ─────────────────────────────────────────────
DB_PATH = os.getenv('DB_PATH', 'dados.db')
SCHEMA_PATH = os.getenv('SCHEMA_PATH', 'schema.sql')

# ── Configuração de Porta Serial ───────────────────────────────────────────────
# Windows: COM3, COM11, etc. | macOS: /dev/tty.usbmodem* | Linux: /dev/ttyUSB0
PORTA_SERIAL = os.getenv('PORTA_SERIAL', 'COM3')
BAUD_RATE = int(os.getenv('BAUD_RATE', '9600'))

# ── Configuração da API ────────────────────────────────────────────────────────
URL_API = os.getenv('URL_API', 'http://localhost:5000/leituras')

# ── Configuração do Flask ──────────────────────────────────────────────────────
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')

# ── Padrões de Dados ───────────────────────────────────────────────────────────
LIMITE_LEITURAS_DEFAULT = int(os.getenv('LIMITE_LEITURAS_DEFAULT', '50'))
LEITURAS_POR_PAGINA = int(os.getenv('LEITURAS_POR_PAGINA', '20'))
