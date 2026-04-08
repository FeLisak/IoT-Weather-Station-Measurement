import re
import serial
import requests

PORTA = '/dev/tty.USB0'
BAUD = 9600
URL = 'http://localhost:5000/leituras'

def ler_serial():
    temperatura = None
    umidade_do_solo = None

    with serial.Serial(PORTA, BAUD, timeout=2) as ser:
        while True:
            linha = ser.readline().decode('utf-8', errors='ignore').strip()
            if not linha:
                continue

            if linha.startswith('Temperatura:'):
                match = re.search(r'[\d.]+', linha)
                if match:
                    temperatura = float(match.group())

            elif linha.startswith('Umidade do solo:'):
                match = re.search(r'\d+', linha)
                if match:
                    umidade_do_solo = int(match.group())

            if temperatura is not None and umidade_do_solo is not None:
                dados = {
                    'temperatura_externa': temperatura,
                    'umidade_do_solo': umidade_do_solo,
                }
                try:
                    requests.post(URL, json=dados)
                    print(f'Enviado: {dados}')
                except requests.exceptions.RequestException as e:
                    print(f'Erro ao enviar: {e}')
                temperatura = None
                umidade_do_solo = None

if __name__ == '__main__':
    ler_serial()
