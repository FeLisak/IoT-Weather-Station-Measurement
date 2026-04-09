import re
import time
import serial
import requests
from config import PORTA_SERIAL, BAUD_RATE, URL_API

INTERVALO_RECONEXAO = 5  # segundos entre tentativas de reconexão


def processar_linha(linha, temperatura, umidade_do_solo):
    if linha.startswith('Temperatura:'):
        match = re.search(r'[\d.]+', linha)
        if match:
            temperatura = float(match.group())
    elif linha.startswith('Umidade do solo:'):
        match = re.search(r'\d+', linha)
        if match:
            umidade_do_solo = int(match.group())
    return temperatura, umidade_do_solo


def enviar_leitura(temperatura, umidade_do_solo):
    dados = {
        'temperatura_externa': temperatura,
        'umidade_do_solo': umidade_do_solo,
    }
    try:
        requests.post(URL_API, json=dados, timeout=5)
        print(f'Enviado: {dados}')
    except requests.exceptions.RequestException as e:
        print(f'Erro ao enviar para API: {e}')


def ler_serial():
    while True:
        try:
            print(f'Conectando à porta {PORTA_SERIAL}...')
            with serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=2) as ser:
                print(f'Conectado em {PORTA_SERIAL} a {BAUD_RATE} baud.')
                temperatura = None
                umidade_do_solo = None

                while True:
                    linha = ser.readline().decode('utf-8', errors='ignore').strip()
                    if not linha:
                        continue

                    temperatura, umidade_do_solo = processar_linha(
                        linha, temperatura, umidade_do_solo
                    )

                    if temperatura is not None and umidade_do_solo is not None:
                        enviar_leitura(temperatura, umidade_do_solo)
                        temperatura = None
                        umidade_do_solo = None

        except serial.SerialException as e:
            if 'PermissionError' in str(e) or 'Acesso negado' in str(e):
                print(
                    f'\nERRO: Acesso negado à porta {PORTA_SERIAL}.\n'
                    'Possíveis causas:\n'
                    '  1. O Serial Monitor do Arduino IDE está aberto — feche-o.\n'
                    '  2. Outra instância deste script já está em execução.\n'
                    '  3. A porta está sendo usada por outro programa.\n'
                    f'Tentando novamente em {INTERVALO_RECONEXAO}s...\n'
                )
            else:
                print(f'Erro na porta serial: {e}')
                print(f'Verifique se a porta "{PORTA_SERIAL}" está correta no arquivo .env')
                print(f'Tentando novamente em {INTERVALO_RECONEXAO}s...')
            time.sleep(INTERVALO_RECONEXAO)

        except KeyboardInterrupt:
            print('\nEncerrado pelo usuário.')
            break


if __name__ == '__main__':
    ler_serial()
