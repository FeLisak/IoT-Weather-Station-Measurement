document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('formEditar');
  const leituraId = form.dataset.leituraId;
  const msg = document.getElementById('formMsg');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const dados = {
      temperatura_externa: parseFloat(document.getElementById('temperatura_externa').value),
      umidade_do_solo: parseFloat(document.getElementById('umidade_do_solo').value),
    };

    try {
      const res = await fetch(`/leituras/${leituraId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados),
      });

      if (res.ok) {
        msg.textContent = 'Leitura atualizada com sucesso!';
        msg.className = 'form-msg success';
        setTimeout(() => (window.location.href = '/historico'), 1200);
      } else {
        const erro = await res.json();
        msg.textContent = `Erro: ${erro.erro}`;
        msg.className = 'form-msg error';
      }
    } catch (e) {
      msg.textContent = 'Erro de comunicação com o servidor.';
      msg.className = 'form-msg error';
    }
  });
});
