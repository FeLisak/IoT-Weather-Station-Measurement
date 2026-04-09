async function deletar(id) {
  if (!confirm(`Excluir leitura #${id}?`)) return;

  try {
    const res = await fetch(`/leituras/${id}`, { method: 'DELETE' });
    if (res.ok) {
      const row = document.getElementById(`row-${id}`);
      row.classList.add('fade-out');
      row.addEventListener('animationend', () => row.remove());
    } else {
      alert('Erro ao excluir a leitura.');
    }
  } catch (e) {
    alert('Erro de comunicação com o servidor.');
  }
}
