fetch('/data')
    .then(response => response.json())
    .then(chartData => {
    var ctx = document.getElementById('YouTubeData').getContext('2d');

    var youtubeChart = new Chart(ctx, {
        type: 'line', 
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Top 50 Videos Time vs. Views',
                    front: {
                        size: 18
                    }
                },
            },
            scales: {
                x: {
                    reverse: true,
                    title: {
                        display: true,
                        text: 'Time'
                    },
                    beginAtZero: false,
                    ticks: {
                        callback: function(value, index, ticks){
                            return value + " day(s)"
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Views'
                    },
                    beginAtZero: true,
                    ticks: {
                        callback: function(value, index, ticks){
                            return value + ' mill';
                        }
                    }
                }
            },
        },
    });
    var index = 0;
    var color = 0;

    updateChartData(() => {
        youtubeChart.data.labels.push(chartData.channel_name[index]);
        youtubeChart.data.datasets[0].data.push(chartData.view_count[index]);
        
        //Having the chart length be at least 
        if(chart.data.labels.length > 50){
            youtubeChart.data.labels.shift();
            youtubeChart.data.datasets[0].data.shift();
        }

        youtubeChart.data.datasets[0].borderColor = 'rgba(${color}, 100, 100)';
        youtubeChart.data.datasets[0].backgroundColor = 'rgba(${color}, 100, 100, 0.1)';

        chart.update();
        index++;
    }, 1000);
});