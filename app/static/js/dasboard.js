async function showProfile(resultId) {
    try {
        const response = await fetch('/api/result/' + resultId);
        const data = await response.json();

        document.getElementById('profileSurname').textContent = data.fullname;
        document.getElementById('profileCallsign').textContent = data.callsign;
        document.getElementById('profileGroup').textContent = data.squad;
        document.getElementById('profileDate').textContent = data.date;

        const statusEl = document.getElementById('profileStatus');
        statusEl.textContent = data.group;
        statusEl.className = 'status-badge';
        if (data.group.includes('СУИЦИДАЛЬНЫЙ') || data.group.includes('ОГРАНИЧИТЬ')) {
            statusEl.classList.add('status-danger');
        } else {
            statusEl.classList.add('status-good');
        }

        document.getElementById('profileConclusion').textContent =
            Array.isArray(data.warnings) && data.warnings.length > 0
                ? data.warnings.join('; ')
                : 'Противопоказаний не выявлено';

        if (data.scores && typeof data.scores === 'object') {
            drawProfileChart(data.scores);
        }

        document.getElementById('profileSection').style.display = 'block';
    } catch (error) {
        const snackbarText = document.querySelector('.snackbar-text')
        const snackbar = document.getElementById('snackbar')
        snackbar.classList.add('active')
        snackbarText.textContent = 'Ошибка загрузки профиля'
        setTimeout(() => {
            snackbar.classList.remove('active')
        }, 3000);
    }
}

function drawProfileChart(scores) {
    const canvas = document.getElementById('profileChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (window.profileChartInstance) window.profileChartInstance.destroy();

    const factors = ['A', 'B', 'C', 'E', 'F', 'G', 'H', 'I', 'L', 'M', 'N', 'O', 'Q1', 'Q2', 'Q3', 'Q4'];
    const values = factors.map(f => scores[f] || 5);

    window.profileChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: factors.map(f => 'Фактор ' + f),
            datasets: [{
                label: 'Стены',
                data: values,
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                borderColor: '#6366f1',
                borderWidth: 2,
                pointBackgroundColor: values.map(v => v >= 7 ? '#10b981' : v <= 4 ? '#ef4444' : '#f59e0b')
            }]
        },
        options: {
            scales: {
                r: {
                    min: 1,
                    max: 10,
                    ticks: {stepSize: 1}
                }
            }
        }
    });
    renderScoresTable(values, factors);
}

function renderScoresTable(values, factors) {
    const valuesContainer = document.getElementById('kattella-panel__values');
    const factorContainer = document.getElementById('kattella-panel__factors');
        valuesContainer.textContent = ''
        factorContainer.textContent = ''

    factors.forEach((factor, index) => {
        const th = document.createElement('th')
        th.classList.add('kattella-panel__cell--header');
        th.textContent = `${factor} (Стен)`

        const td = document.createElement('td')
        td.classList.add('kattella-panel__cell');
        td.textContent = values[index];


        valuesContainer.append(td)
        factorContainer.append(th)

    })

}

function deleteResult(resultId) {
    if (confirm('Удалить результат?')) {
        fetch('/api/result/' + resultId, {method: 'DELETE'})
            .then(r => r.json())
            .then(d => {
                if (d.success) location.reload();
                else alert('Ошибка удаления');
            });
    }
}