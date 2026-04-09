from flask import Flask, jsonify, request, render_template, abort
from database import init_db, inserir_leitura, listar_leituras, buscar_leitura, atualizar_leitura, deletar_leitura
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

app = Flask(__name__)


# ── Páginas ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    leituras = listar_leituras(limite=10)
    return render_template('index.html', leituras=leituras)


@app.route('/historico')
def historico():
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = 20
    todas = listar_leituras(limite=por_pagina * pagina)
    leituras = todas[(pagina - 1) * por_pagina: pagina * por_pagina]
    tem_proxima = len(todas) == por_pagina * pagina
    return render_template(
        'histórico.html',
        leituras=leituras,
        pagina=pagina,
        tem_proxima=tem_proxima,
    )


@app.route('/editar/<int:id>')
def editar(id):
    leitura = buscar_leitura(id)
    if leitura is None:
        abort(404)
    return render_template('editar.html', leitura=leitura)


# ── API REST ───────────────────────────────────────────────────────────────────

@app.route('/leituras', methods=['GET'])
def api_listar():
    limite = request.args.get('limite', 50, type=int)
    return jsonify(listar_leituras(limite=limite))


@app.route('/api/grafico', methods=['GET'])
def api_grafico():
    """Retorna dados formatados para o gráfico de variação temporal."""
    leituras = listar_leituras(limite=100)
    # Inverte a ordem para ter as datas em ordem cronológica
    leituras = list(reversed(leituras))
    
    return jsonify({
        'timestamps': [l['timestamp'] for l in leituras],
        'temperaturas': [l['temperatura_externa'] for l in leituras],
        'umidades': [l['umidade_do_solo'] for l in leituras],
    })


@app.route('/leituras', methods=['POST'])
def api_criar():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400
    campos = {'temperatura_externa', 'umidade_do_solo'}
    faltando = campos - dados.keys()
    if faltando:
        return jsonify({'erro': f'Campos obrigatórios ausentes: {faltando}'}), 400
    id_novo = inserir_leitura(dados['temperatura_externa'], dados['umidade_do_solo'])
    return jsonify({'id': id_novo, 'status': 'criado'}), 201


@app.route('/leituras/<int:id>', methods=['GET'])
def api_buscar(id):
    leitura = buscar_leitura(id)
    if leitura is None:
        return jsonify({'erro': 'Não encontrado'}), 404
    return jsonify(leitura)


@app.route('/leituras/<int:id>', methods=['PUT'])
def api_atualizar(id):
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400
    atualizado = atualizar_leitura(id, dados)
    if not atualizado:
        return jsonify({'erro': 'Não encontrado'}), 404
    return jsonify({'status': 'atualizado'})


@app.route('/leituras/<int:id>', methods=['DELETE'])
def api_deletar(id):
    deletado = deletar_leitura(id)
    if not deletado:
        return jsonify({'erro': 'Não encontrado'}), 404
    return jsonify({'status': 'deletado'})


# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
