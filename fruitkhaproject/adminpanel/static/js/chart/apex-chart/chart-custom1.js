//bar chart
document.addEventListener('DOMContentLoaded', function () {
    // Retrieve the monthly revenue data from the data attribute
    var monthlyRevenueData = JSON.parse(document.getElementById('bar-chart-earning').getAttribute('data-monthly-revenue'));
    var monthlyordersdata = JSON.parse(document.getElementById('bar-chart-earning').getAttribute('data-monthly-orders'));


var options = {
    series: [{
            name: " Total Revenue",
            data : monthlyRevenueData,
        },

        {
            name: "Total Orders",
            data: monthlyordersdata,
        }
    ],

    chart: {
        toolbar: {
            show: false
        }
    },

    chart: {
        height: 320,
    },

    legend: {
        show: false,
    },

    colors: ['#e22454', '#2483e2'],

    markers: {
        size: 1,
    },

    // grid: {
    //     show: false,
    //     xaxis: {
    //         lines: {
    //             show: false
    //         }
    //     },
    // },

    xaxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','aug','sep','oct','Nov','dec'],
        labels: {
            show: false,
        }
    },

    responsive: [{
            breakpoint: 1400,
            options: {
                chart: {
                    height: 300,
                },
            },
        },

        {
            breakpoint: 992,
            options: {
                chart: {
                    height: 210,
                    width: "100%",
                    offsetX: 0,
                },
            },
        },

        {
            breakpoint: 578,
            options: {
                chart: {
                    height: 200,
                    width: "105%",
                    offsetX: -20,
                    offsetY: 10,
                },
            },
        },

        {
            breakpoint: 430,
            options: {
                chart: {
                    width: "108%",
                },
            },
        },

        {
            breakpoint: 330,
            options: {
                chart: {
                    width: "118%",
                },
            },
        },
    ],
};

var chart = new ApexCharts(document.querySelector("#bar-chart-earning"), options);
chart.render();
});
// expenses cart


document.addEventListener('DOMContentLoaded', function () {
    // Retrieve the yearly revenue data from the data attribute
    var YearlyRevenueData = JSON.parse(document.getElementById('report-chart').getAttribute('data-yearly-orders'));
    var data = [];

    // Assuming YearlyRevenueData is an array of yearly revenue values
    for (var i = 0; i < YearlyRevenueData.length; i++) {
        var year = 2023 + i; // Adjust the year based on the index
        var yearlyValue = YearlyRevenueData[i]; // Use the yearly revenue value

        data.push({
            x: year.toString(),
            y: yearlyValue,
            goals: [{
                name: 'Expected',
                value: Math.floor(Math.random() * 10000), // Generate random expected value
                strokeWidth: 5,
                strokeColor: '#775DD0' // Keep stroke color consistent
            }]
        });
    }

    // Chart options
    var options = {
        series: [{
            name: 'Total Revenue',
            data: data,
        }],
        chart: {
            height: 320,
            type: 'bar'
        },
        plotOptions: {
            bar: {
                columnWidth: '20%'
            }
        },
        dataLabels: {
            enabled: false
        },
        legend: {
            show: false,
        }
    };

    // Render the chart
    var chart = new ApexCharts(document.querySelector("#report-chart"), options);
    chart.render();
});

//pie chart for visitors
var options = {
    series: [44, 55, 41, 17],
    labels: ['The Passersby', 'The Occasionals', 'The Regulars', 'The Superfans'],
    chart: {
        width: "100%",
        height: 275,
        type: 'donut',
    },

    legend: {
        fontSize: '12px',
        position: 'bottom',
        offsetX: 1,
        offsetY: -1,

        markers: {
            width: 10,
            height: 10,
        },

        itemMargin: {
            vertical: 2
        },
    },

    colors: ['#4aa4d9', '#ef3f3e', '#9e65c2', '#6670bd', '#FF9800'],

    plotOptions: {
        pie: {
            startAngle: -90,
            endAngle: 270
        }
    },

    dataLabels: {
        enabled: false
    },

    responsive: [{
            breakpoint: 1835,
            options: {
                chart: {
                    height: 245,
                },

                legend: {
                    position: 'bottom',

                    itemMargin: {
                        horizontal: 5,
                        vertical: 1
                    },
                },
            },
        },

        {
            breakpoint: 1388,
            options: {
                chart: {
                    height: 330,
                },

                legend: {
                    position: 'bottom',
                },
            },
        },

        {
            breakpoint: 1275,
            options: {
                chart: {
                    height: 300,
                },

                legend: {
                    position: 'bottom',
                },
            },
        },

        {
            breakpoint: 1158,
            options: {
                chart: {
                    height: 280,
                },

                legend: {
                    fontSize: '10px',
                    position: 'bottom',
                    offsetY: 10,
                },
            },
        },

        {
            theme: {
                mode: 'dark',
                palette: 'palette1',
                monochrome: {
                    enabled: true,
                    color: '#255aee',
                    shadeTo: 'dark',
                    shadeIntensity: 0.65
                },
            },
        },

        {
            breakpoint: 598,
            options: {
                chart: {
                    height: 280,
                },

                legend: {
                    fontSize: '12px',
                    position: 'bottom',
                    offsetX: 5,
                    offsetY: -5,

                    markers: {
                        width: 10,
                        height: 10,
                    },

                    itemMargin: {
                        vertical: 1
                    },
                },
            },
        },
    ],
};

var chart = new ApexCharts(document.querySelector("#pie-chart-visitors"), options);
chart.render();