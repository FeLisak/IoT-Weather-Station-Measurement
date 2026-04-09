let timer;
let graficoInstance = null;

function pulsar() {
  const dot = document.getElementById('refreshIndicator').querySelector('.dot');
  dot.classList.add('pulse');
  setTimeout(() => dot.classList.remove('pulse'), 600);
}

async function carregarGrafico() {
  try {
    const res = await fetch('/api/grafico');
    const dados = await res.json();

    const ctx = document.getElementById('graficoVariacao').getContext('2d');

    if (graficoInstance) {
      graficoInstance.destroy();
    }

    const labelsFormatados = dados.timestamps.map((ts) => {
      if (!ts) return '';
      const data = new Date(ts.replace(' ', 'T'));
      return (
        data.toLocaleDateString('pt-BR', { month: 'short', day: 'numeric' }) +
        ' ' +
        data.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
      );
    });

    graficoInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labelsFormatados,
        datasets: [
          {
            label: 'Temperatura (°C)',
            data: dados.temperaturas,
            borderColor: '#FF6B6B',
            backgroundColor: 'rgba(255, 107, 107, 0.1)',
            tension: 0.4,
            fill: true,
            pointRadius: 4,
            pointBackgroundColor: '#FF6B6B',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            yAxisID: 'y',
          },
          {
            label: 'Umidade do Solo',
            data: dados.umidades,
            borderColor: '#4ECDC4',
            backgroundColor: 'rgba(78, 205, 196, 0.1)',
            tension: 0.4,
            fill: true,
            pointRadius: 4,
            pointBackgroundColor: '#4ECDC4',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            yAxisID: 'y1',
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: { usePointStyle: true, padding: 15, font: { size: 12 } },
          },
          tooltip: {
            backgroundColor: 'rgba(0,0,0,0.8)',
            padding: 12,
            titleFont: { size: 12 },
            bodyFont: { size: 11 },
          },
        },
        scales: {
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            title: { display: true, text: 'Temperatura (°C)', color: '#FF6B6B' },
            ticks: { color: '#FF6B6B' },
          },
          y1: {
            type: 'linear',
            display: true,
            position: 'right',
            title: { display: true, text: 'Umidade do Solo', color: '#4ECDC4' },
            ticks: { color: '#4ECDC4' },
            grid: { drawOnChartArea: false },
          },
        },
      },
    });
  } catch (e) {
    console.error('Erro ao carregar gráfico:', e);
  }
}

async function atualizarCards() {
  try {
    const res = await fetch(`/leituras?limite=${CONFIG.LIMITE_DASHBOARD}`);
    const dados = await res.json();
    const container = document.getElementById('cardsContainer');

    if (!dados.length) return;

    container.innerHTML = dados
      .map(
        (l) => `
        <div class="card">
          <div class="card-id">#${l.id}</div>
          <div class="card-body">
            <div class="metric">
              <span class="metric-icon">🌡️</span>
              <div>
                <div class="metric-label">Temperatura</div>
                <div class="metric-value">${l.temperatura_externa.toFixed(1)} °C</div>
              </div>
            </div>
            <div class="metric">
              <span class="metric-icon">💧</span>
              <div>
                <div class="metric-label">Umidade do Solo</div>
                <div class="metric-value">${l.umidade_do_solo} <small>/ 1023</small></div>
              </div>
            </div>
          </div>
          <div class="card-footer">
            <span class="timestamp">${l.timestamp}</span>
            <a href="/editar/${l.id}" class="btn btn-sm btn-edit">Editar</a>
          </div>
        </div>
      `
      )
      .join('');

    pulsar();
    carregarGrafico();
  } catch (e) {
    console.error('Erro ao atualizar:', e);
  }
}

function iniciarAutoRefresh() {
  timer = setInterval(atualizarCards, CONFIG.INTERVALO_REFRESH);
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btnAtualizar').addEventListener('click', () => {
    clearInterval(timer);
    atualizarCards();
    iniciarAutoRefresh();
  });

  atualizarCards();
  iniciarAutoRefresh();
});
