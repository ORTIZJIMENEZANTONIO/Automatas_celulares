/*
$(window).on('load', function(){

    var ctx = $('#column-chart');

 
    var chartOptions = {
        elements: {
            rectangle: {
                borderWidth: 2,
                borderColor: 'rgb(0, 255, 0)',
                borderSkipped: 'bottom'
            }
        },
        responsive: true,
        maintainAspectRatio: false,
        responsiveAnimationDuration:500,
        legend: {
            position: 'top',
        },
        scales: {
            xAxes: [{
                display: true,
                gridLines: {
                    color: '#f3f3f3',
                    drawTicks: false,
                },
                scaleLabel: {
                    display: true,
                }
            }],
            yAxes: [{
                display: true,
                gridLines: {
                    color: '#f3f3f3',
                    drawTicks: false,
                },
                scaleLabel: {
                    display: true,
                }
            }]
        }
       
    };

    var chartData = {
        labels: ['G-1', 'G-2', 'G-3', 'G-4', 'G-5', 'G-6'],
        datasets: [{
            label: '0',
            data: [65, 85, 40, 81, 56, 75],
            backgroundColor: '#28D094',
            hoverBackgroundColor: 'rgba(40,208,148,.9)',
            borderColor: 'transparent'
        }, {
            label: '1',
            data: [45, 65, 65, 19, 86, 35],
            backgroundColor: '#FF4961',
            hoverBackgroundColor: 'rgba(255,73,97,.9)',
            borderColor: 'transparent'
        }]
    };

    var config = {
        type: 'bar',

        options : chartOptions,

        data : chartData
    };

    var lineChart = new Chart(ctx, config);
});
*/