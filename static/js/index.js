var options = {
    chart: {
        type: 'bar',
        height: '300px',
        toolbar: {
            show: false,
        },
    },
    series: [{
        name: '学習回数',
        data: [30, 40, 35, 50, 49, 60, 70, 91, 125]
    },
    {
        name: '正解数',
        data: [49, 60, 70, 91, 125, 30, 40, 35, 50]
    }],
    xaxis: {
        categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]
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