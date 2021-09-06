var dates = JSON.parse($('#dates').data('values').replaceAll('\'', '"'));
var learning_counts = $('#learning_counts').data('values');
var correct_counts = $('#correct_counts').data('values');


var options = {
    chart: {
        type: 'bar',
        height: '300px',
        toolbar: {
            show: false,
        },
    },
    series: [
        {
            name: '学習回数',
            data: learning_counts,
        },
        {
            name: '正解数',
            data: correct_counts,
        },
    ],
    xaxis: {
        categories: dates
    },
    legend: {
        show: true,
        horizontalAlign: 'right',
        position: 'top',
    },
    theme: {
        monochrome: {
            enabled: true,
            color: '#255aee',
            shadeTo: 'light',
            shadeIntensity: 0.65
        }
    },
    
}

var chart = new ApexCharts(document.querySelector("#chart"), options);

chart.render();