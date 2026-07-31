/*===== sidebar =====*/
const sidebar = document.getElementById('sidebar');
const buttonSidebar = document.getElementById('sidebar-toggle');
const iconButton = document.querySelector('.icon-btn');
const sidebarText = document.querySelectorAll('.slider-nav--text');
const sidebarCard = document.querySelector('.user-card__info');
const sidebarLogout = document.querySelector('.user__logout');


buttonSidebar.addEventListener('click', closeSidebar);

function closeSidebar() {
    sidebar.classList.toggle('active');
    iconButton.classList.toggle('rotate-180');
    sidebarText.forEach(item => item.classList.toggle('slider-nav--text-close'));
    sidebarCard.classList.toggle('user-card__info--close');
    sidebarLogout.classList.toggle('user__logout--close');

    const state = sidebar.classList.contains('active') ? 'open' : 'close';
    localStorage.setItem('sidebar', state);
}

document.addEventListener('DOMContentLoaded', function() {
    const state = localStorage.getItem('sidebar');

    if (state === 'open') {
        sidebar.classList.add('active');
        iconButton.classList.add('rotate-180');
        sidebarText.forEach(item => item.classList.add('slider-nav--text-close'));
        sidebarCard.classList.add('user-card__info--close');
        sidebarLogout.classList.add('user__logout--close');
    }
});

async function showProfile(resultId) {
    const skeleton = document.getElementById('profileSkeleton');
    skeleton.style.display = 'flex';
    try {
        const response = await fetch('/api/result/' + resultId);
        if (!response.ok) {
            throw new Error(response.statusText);
        }
        const data = await response.json();
        document.getElementById('profileSurname').textContent = `${data.fullname}`;
        document.getElementById('profileCallsign').textContent = `${data.callsign} ·`;
        document.getElementById('profileGroup').textContent = `${data.squad} ·`;
        document.getElementById('profileDate').textContent = `${data.date}`;
        const statusEl = document.getElementById('profileStatus');
        statusEl.textContent = data.group;
        statusEl.className = 'status-badge';
        if (data.group.includes('СУИЦИДАЛЬНЫЙ') || data.group.includes('ОГРАНИЧИТЬ')) {
            statusEl.classList.add('status-danger');
        } else {
            statusEl.classList.add('status-good');
        }
        document.getElementById('profileConclusion').textContent = Array.isArray(data.warnings) && data.warnings.length > 0 ? data.warnings.join('; ') : 'Противопоказаний не выявлено';
        if (data.scores && typeof data.scores === 'object' || data.news_scores && typeof data.news_scores === 'object') {
            drawProfileChart(data.scores, data.news_scores);
        }

        document.getElementById('profileSection').style.display = 'block';

        const profileContainer = document.getElementById('profileSection');

        profileContainer.style.height = 'auto';
        profileContainer.style.opacity = '0';
        profileContainer.classList.add('active');

        const fullHeight = profileContainer.offsetHeight;

        profileContainer.style.height = '0px';
        profileContainer.style.opacity = '1';

        requestAnimationFrame(function () {
            profileContainer.style.height = fullHeight + 'px';
        });

        skeleton.style.display = 'none';

    } catch (error) {
        alert(error);
    }
}

function drawProfileChart(scores, new_scores) {
    const canvas = document.getElementById('profileChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (window.profileChartInstance) window.profileChartInstance.destroy();
    const factors = ['A', 'B', 'C', 'E', 'F', 'G', 'H', 'I', 'L', 'M', 'N', 'O', 'Q1', 'Q2', 'Q3', 'Q4'];
    const values = factors.map(f => scores[f] || 5);
    const valuesScore = factors.map(f => new_scores[f] || 5);

    window.profileChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: factors.map(f => 'Фактор ' + f),
            datasets: [{
                label: 'Стены',
                data: values,
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                borderColor: '#6366f1',
                borderWidth: 3,
                pointBackgroundColor: values.map(v => v >= 7 ? '#10b981' : v <= 4 ? '#ef4444' : '#f59e0b'),
                pointRadius: 6,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    min: 1,
                    max: 10,
                    ticks: {
                        stepSize: 1,
                        backdropColor: 'transparent',
                        font: {size: 11}
                    },
                    grid: {color: '#e2e8f0'},
                    angleLines: {color: '#e2e8f0'},
                    pointLabels: {
                        font: {size: 10, weight: '600'}
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        font: {size: 12}
                    }
                }
            }

        }
    });
    renderScoresTable(values, factors, valuesScore);
}

function renderScoresTable(values, factors, valuesScore) {
    const valuesContainer = document.getElementById('kattella-panel__values');
    const factorContainer = document.getElementById('kattella-panel__factors');
    const scoresContainer = document.getElementById('kattella-panel__scores');
    const scoresValuesContainer = document.getElementById('kattella-panel__scores-values');

    valuesContainer.innerHTML = ''
    factorContainer.innerHTML = ''
    scoresContainer.innerHTML = ''
    scoresValuesContainer.innerHTML = ''

    factors.forEach((factor, index) => {
        const factors = document.createElement('th')
        factors.classList.add('kattella-panel__cell--header');
        factors.textContent = `${factor}(Стен)`

        const newValues = document.createElement('td')
        newValues.classList.add('kattella-panel__cell');
        newValues.textContent = values[index];

        valuesContainer.append(newValues)
        factorContainer.append(factors)

    })

    factors.forEach((factor, index) => {
        const scoresFactors = document.createElement('th')
        scoresFactors.classList.add('kattella-panel__cell--header');
        scoresFactors.textContent = `Фактор ${factor} (Сырой)`

        const scoresValues = document.createElement('td')
        scoresValues.classList.add('kattella-panel__cell');
        scoresValues.textContent = valuesScore[index];

        scoresContainer.append(scoresFactors)
        scoresValuesContainer.append(scoresValues)
    })

}

function deleteResult(resultId) {
    const overlayContainer = document.getElementById('confirmOverlay');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

    overlayContainer.classList.add('active');

    confirmDeleteBtn.addEventListener('click', function () {
        fetch('/api/result/' + resultId, {method: 'DELETE'}).then(r => r.json()).then(d => {
            if (d.success) location.reload(); else alert('Ошибка удаления');
        });
    })
}

function closeConfirm() {
    const overlayContainer = document.getElementById('confirmOverlay');
    overlayContainer.classList.remove('active');
}

function downloaditem(resultId) {
}



