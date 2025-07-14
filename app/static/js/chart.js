const ctx = document.getElementById('keywordChart').getContext('2d');
const chartData = JSON.parse(document.getElementById('chart-data').textContent);

const chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: chartData.labels,
        datasets: [{
            label: 'Keyword Frequency',
            data: chartData.values,
            backgroundColor: 'rgba(54, 162, 235, 0.7)'
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
