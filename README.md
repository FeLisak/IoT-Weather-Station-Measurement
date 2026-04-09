# Sistema de Medição de Estação Meteorológica IoT

Atividade ponderada do Módulo 5 — Automação de Processos e Sistemas.

**Integrantes:** Felipe Karpovas Lisak e Gabriel Mutter de Souza

O objetivo foi construir um sistema completo de ponta a ponta: um dispositivo físico (Arduino com sensor DHT11) que envia leituras de temperatura e umidade do solo via porta serial para um servidor Flask, que armazena os dados em SQLite e os exibe em uma interface web.

---

## Decisões de Arquitetura

A atividade sugeria um schema com os campos genéricos `temperatura` e `umidade`. Optamos por renomeá-los para refletir melhor o que o sensor realmente mede:

| Campo sugerido | Campo utilizado       | Motivo                                                               |
| -------------- | --------------------- | -------------------------------------------------------------------- |
| `temperatura`  | `temperatura_externa` | Deixa explícito que é a temperatura do ambiente externo              |
| `umidade`      | `umidade_do_solo`     | O sensor DHT11 mede umidade relativa, aqui interpretada como do solo |

O fluxo de dados seguiu a arquitetura proposta:

```
Arduino → Porta Serial USB → serial_reader.py → POST /leituras → SQLite → Interface Web
```

---

## Estrutura do Projeto

```
IoT-Weather-Station-Measurement/
├── app.py              # Servidor Flask: rotas de páginas e API REST
├── config.py           # Configuração centralizada (lê variáveis do .env)
├── database.py         # Funções de acesso ao banco (CRUD)
├── serial_reader.py    # Leitura da porta serial com reconexão automática
├── schema.sql          # Schema da tabela + 30 registros de exemplo
├── .env.example        # Modelo de variáveis de ambiente
├── static/
│   ├── css/style.css   # Estilos da interface
│   └── js/
│       ├── config.js   # Constantes de configuração do frontend
│       ├── main.js     # JavaScript compartilhado (navbar ativa)
│       ├── dashboard.js # Gráfico, cards e auto-refresh do painel
│       ├── historico.js # Exclusão de leituras no histórico
│       └── editar.js   # Submissão assíncrona do formulário de edição
├── templates/
│   ├── base.html       # Layout base (navbar, container)
│   ├── index.html      # Painel principal
│   ├── histórico.html  # Tabela de leituras com paginação e exclusão
│   └── editar.html     # Formulário de edição de uma leitura
├── arduino/
│   └── estacao.ino     # Sketch do Arduino
└── README.md
```

---

## Pré-requisitos

- Python 3.10 ou superior
- Arduino IDE 2.x (se for usar o hardware físico)
- Sensor DHT11 conectado ao Arduino (pino digital 2)

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/FeLisak/IoT-Weather-Station-Measurement.git
cd IoT-Weather-Station-Measurement

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install flask pyserial python-dotenv

# Configure as variáveis de ambiente
cp .env.example .env
# Edite .env conforme seu ambiente (porta serial, etc.)
```

---

## Como executar

### 1. Iniciar o servidor Flask

```bash
python app.py
```

O banco de dados é criado automaticamente na primeira execução com 30 leituras de exemplo. Acesse `http://localhost:5000` no navegador.

### 2. Iniciar a leitura serial (com Arduino conectado)

Em outro terminal:

```bash
python serial_reader.py
```

Configure a porta serial no arquivo `.env`:

```env
# Windows
PORTA_SERIAL=COM3

# macOS
PORTA_SERIAL=/dev/tty.usbmodem14101

# Linux
PORTA_SERIAL=/dev/ttyUSB0
```

O `serial_reader.py` reconecta automaticamente em caso de falha ou porta ocupada (ex.: Serial Monitor do Arduino IDE aberto), sem necessidade de reiniciar manualmente.

---

## Banco de Dados

O schema da tabela `leituras`:

```sql
CREATE TABLE IF NOT EXISTS leituras (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  temperatura_externa REAL NOT NULL,
  umidade_do_solo     REAL NOT NULL,
  timestamp           DATETIME DEFAULT (datetime('now','localtime'))
);
```

> Configuramos `PRAGMA journal_mode=WAL` na conexão para permitir que o Flask e o `serial_reader.py` escrevessem no banco simultaneamente sem travar um ao outro.

O arquivo `schema.sql` inclui 30 registros de exemplo com variações realistas de temperatura e umidade, inseridos com `INSERT OR IGNORE` para não sobrescrever dados existentes ao reinicializar.

---

## API REST

| Método   | Rota                  | Descrição                                        |
| -------- | --------------------- | ------------------------------------------------ |
| `GET`    | `/`                   | Painel principal (últimas 10 leituras)           |
| `GET`    | `/historico?pagina=N` | Histórico paginado (20 por página)               |
| `GET`    | `/editar/<id>`        | Formulário de edição                             |
| `GET`    | `/leituras`           | Lista leituras em JSON                           |
| `GET`    | `/api/grafico`        | Dados de temperatura e umidade para o gráfico   |
| `POST`   | `/leituras`           | Insere nova leitura                              |
| `GET`    | `/leituras/<id>`      | Retorna uma leitura específica                   |
| `PUT`    | `/leituras/<id>`      | Atualiza uma leitura                             |
| `DELETE` | `/leituras/<id>`      | Remove uma leitura                               |

### Exemplos com curl

```bash
# Inserir uma leitura manualmente
curl -X POST http://localhost:5000/leituras \
  -H "Content-Type: application/json" \
  -d '{"temperatura_externa": 24.5, "umidade_do_solo": 450}'

# Listar leituras
curl http://localhost:5000/leituras

# Atualizar
curl -X PUT http://localhost:5000/leituras/1 \
  -H "Content-Type: application/json" \
  -d '{"temperatura_externa": 25.0}'

# Deletar
curl -X DELETE http://localhost:5000/leituras/1
```

---

## Interface Web

Três páginas foram desenvolvidas:

**Painel (`/`)** — exibe as 10 leituras mais recentes em cards, um gráfico de variação temporal de temperatura e umidade (últimos 100 registros via Chart.js) e atualização automática a cada 30 segundos com botão de atualização manual.

**Histórico (`/historico`)** — apresenta uma tabela com paginação (20 registros por página) e botão de exclusão por linha com animação de remoção.

**Edição (`/editar/<id>`)** — traz um formulário pré-preenchido com os valores atuais da leitura; a submissão é feita via `PUT` sem recarregar a página, redirecionando ao histórico após salvar.

---

## Arduino

O sketch `arduino/estacao.ino` utilizou:

- Sensor **DHT11** (pino digital 2) para leitura de temperatura
- Sensor analógico de umidade do solo (pino **A0**), que retorna um valor bruto entre 0 e 1023

O Arduino envia as leituras pela serial em texto puro, a cada 2 segundos, no seguinte formato:

```
Temperatura: 23.40 °C
Umidade do solo: 450
O solo está: Úmido
```

O `serial_reader.py` faz o parse dessas linhas com regex e envia os dados ao servidor via `POST /leituras` após acumular os dois valores de cada ciclo.

> Caso não haja o hardware disponível, é possível testar o sistema inserindo leituras manualmente via `curl` ou Postman:
>
> ```bash
> curl -X POST http://localhost:5000/leituras \
>   -H "Content-Type: application/json" \
>   -d '{"temperatura_externa": 23.4, "umidade_do_solo": 450}'
> ```
