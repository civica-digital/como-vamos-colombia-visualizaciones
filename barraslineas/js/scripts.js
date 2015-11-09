$(function () {
    $('#container').highcharts({
        chart: {
            zoomType: 'xy'
        },
        title: {
            text: '¿Existen oportunidades laborales en la ciudad? vs Indice de Desempleo en Medellín'
        },
        xAxis: [{
            categories: ['2005', '2006', '2007', '2008', '2009', '2010',
                '2011', '2012', '2013', '2014'],
            crosshair: true
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value}',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            title: {
                text: '',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            }
        }, { // Secondary yAxis
            title: {
                text: '% de Encuestados',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            labels: {
                format: '{value}',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            opposite: true
        }],
        tooltip: {
            shared: true
        },
        credits: {
    enabled: false
        },
        plotOptions: {
            column: {
                stacking: 'normal'
            }
        },
        series: [{
            name: 'Si',
            type: 'column',
            yAxis: 1,
            data: [0, 0, 0, 0, 0 , 0, 0.6175, 0.39, 0.45, 0],
            tooltip: {
                valueSuffix: ' % de Encuestados'
            },
			stack: "1",
        }, {
            name: 'No',
            type: 'column',
            yAxis: 1,
            data: [0, 0, 0, 0, 0 , 0, 0.3825, 0.61, 0.55, 0],
            tooltip: {
                valueSuffix: ' % de Encuestados'
            },
			stack: "1",
        }, {
            name: 'Índice de Desempleo',
            type: 'spline',
            data: [0.137679449,0.13449362,0.12050198,0.135813811,0.156584082,0.138943827,0.122501056,0.124101423,0.112241421,0.102],
            tooltip: {
                valueSuffix: ' S/U'
            }
        }]
    });
});
