document.addEventListener('DOMContentLoaded', function () {
    function initializeChart(ctxId, labelsId, dataIds, config) {
        const ctx = document.getElementById(ctxId)?.getContext('2d');
        if (ctx) {
            const labels = JSON.parse(document.getElementById(labelsId).textContent);
            config.data.labels = labels;

            // Veriyi birden fazla dataset için düzenleme
            config.data.datasets = dataIds.map((dataId, index) => {
                const data = JSON.parse(document.getElementById(dataId).textContent);
                return {
                    label: config.datasetLabels[index],
                    data: data,
                    backgroundColor: config.datasetColors[index].backgroundColor,
                    borderColor: config.datasetColors[index].borderColor,
                    borderWidth: 1,
                };
            });

            new Chart(ctx, config);
        }
    }

    // Terapist Performansı Grafiği
    initializeChart(
        'performanceChart',
        'performance-labels',
        ['performance-scheduled', 'performance-completed', 'performance-cancelled'],
        {
            type: 'bar',
            datasetLabels: ['Planlanan', 'Gerçekleşen', 'İptal Edilen'],
            datasetColors: [
                { backgroundColor: 'rgba(75, 192, 192, 0.2)', borderColor: 'rgba(75, 192, 192, 1)' },
                { backgroundColor: 'rgba(54, 162, 235, 0.2)', borderColor: 'rgba(54, 162, 235, 1)' },
                { backgroundColor: 'rgba(255, 99, 132, 0.2)', borderColor: 'rgba(255, 99, 132, 1)' },
            ],
            data: { labels: [], datasets: [] },
            options: { scales: { y: { beginAtZero: true } } },
        }
    );

    // Randevular Grafiği
    initializeChart(
        'appointmentsChart',
        'chart-labels',
        ['chart-data'],
        {
            type: 'bar',
            datasetLabels: ['Randevu Sayısı'],
            datasetColors: [{ backgroundColor: 'rgba(54, 162, 235, 0.2)', borderColor: 'rgba(54, 162, 235, 1)' }],
            data: { labels: [], datasets: [] },
            options: { scales: { y: { beginAtZero: true } } },
        }
    );

    // Zaman Serisi Grafiği
    initializeChart(
        'timeSeriesChart',
        'chart-labels',
        ['chart-data'],
        {
            type: 'line',
            datasetLabels: ['Günlük Randevu Sayısı'],
            datasetColors: [{ borderColor: 'rgba(255, 99, 132, 1)' }],
            data: { labels: [], datasets: [] },
            options: { scales: { y: { beginAtZero: true } } },
        }
    );
});
