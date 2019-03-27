window.onload = function() {

    $('#start_message').html(`
		<div>
    		<h1>Input Actual CTR Values (<i>in [0.0-1.0] range):</i></h1>
		</div>`).show();
}

$(document).on('submit', '#form', (event) => {
    event.preventDefault()
    const CTR1 = $('#CTR1').val()
    const CTR2 = $('#CTR2').val()
    getDouble(CTR1, CTR2)
})

async function getDouble(CTR1, CTR2) {
    const response = await fetch('/process', {
        method: 'POST',
        body: JSON.stringify({
            CTR1: CTR1,
            CTR2: CTR2,
        }),
        headers: {
            'Content-Type': 'application/json',
        },
    })

    if (!response.ok) {
        render(true, [])
        return
    }

    const data = await response.json()
    render(data)
}



function numberRange (start, end) {
  return new Array(end - start).fill().map((d, i) => i + start);
}

function render(data) {
    console.log(data)
//    document.getElementById("output_rs").innerHTML = data.output_rs
//    document.getElementById("output_eg").innerHTML = data.output_eg
//    document.getElementById("output_ts").innerHTML = data.output_ts
//    document.getElementById("output_ucb1").innerHTML = data.output_ucb1


//    var chart = c3.generate({
//        data: {
//            columns: [
//                ['Random Sampling', data.reward_rs],
//                ['Epsilon Greedy', data.reward_eg],
//                ['Thompson Sampling', data.reward_ts],
//                ['UCB1', data.reward_ucb1],
//            ],
//            type: 'bar'
//        },
//        axis: {
//        rotated: true,
//        x: {
//            type: 'category',
//            categories: ['Algorithms']
//                    }
//            },
//        bindto: '#reward_chart'
//    });

//    var chart = c3.generate({
//        data: {
//            columns: [
//                ['Ad #1', data.ad_1_rs, data.ad_1_eg, data.ad_1_ts, data.ad_1_ucb1],
//                ['Ad #2', data.ad_2_rs, data.ad_2_eg, data.ad_2_ts, data.ad_2_ucb1]
//            ],
//            type: 'bar',
//            groups: [
//                ['Ad #1', 'Ad #2']
//            ]
//        },
//        grid: {
//            y: {
//                lines: [{value:0}]
//            }
//        },
//        axis: {
//        x: {
//            type: 'category',
//            categories: ['Random Sampling', 'Epsilon Greedy', 'Thompson Sampling', 'UCB1']
//                    }
//            },
//        bindto: '#ad_chart'
//    });

    var container_rew = document.getElementById('reward_chart');
    var data_rew = {
        categories: ['Algorithm'],
        series: [
            {
                name: 'Random Sampling',
                data: [data.reward_rs]
            },
            {
                name: 'Epsilon Greedy',
                data: [data.reward_eg]
            },
            {
                name: 'Thompson Sampling',
                data: [data.reward_ts]
            },
            {
                name: 'UCB1',
                data: [data.reward_ts]
            }
        ]
    };
    var options_rew = {
        chart: {
            width: 1100,
            height: 450,
            title: 'Reward by the Algorithm',
            format: '1,000'
        },
//        yAxis: {
//            title: 'Month'
//        },
        xAxis: {
            title: 'Reward',
            min: 0
        },
         series: {
             showLabel: true
         }
    };
    var theme_rew = {
        series: {
            colors: [
                 '#ffcc66', '#0099ff', '#ff3300', '#33cc33'
            ]
        }
    };
    tui.chart.registerTheme('Reward_theme', theme_rew);
    options_rew.theme = 'Reward_theme';
    tui.chart.barChart(container_rew, data_rew, options_rew);

    var container_a = document.getElementById('ad_chart');
    var data_a = {
        categories: ['Random Sampling', 'Epsilon Greedy', 'Thompson Sampling', 'UCB1'],
        series: [
            {
                name: 'Ad #1',
                data: [data.ad_1_rs, data.ad_1_eg, data.ad_1_ts, data.ad_1_ucb1]
            },
            {
                name: 'Ad #2',
                data: [data.ad_2_rs, data.ad_2_eg, data.ad_2_ts, data.ad_2_ucb1]
            }
        ]
    };
    var options_a = {
        chart: {
            width: 1100,
            height: 450,
            title: 'Ratio of Ads Appearance Throughout the Trials',
            format: '1,000'
        },
        yAxis: {
            title: 'Ratio',
            min: 0,
            max: 1
        },
        xAxis: {
            title: 'Algorithm'
        },
        series: {
            stackType: 'normal'
        },
        tooltip: {
            grouped: true
        },
        legend: {
            align: 'bottom4000'
        }
    };
    var theme_a = {
        series: {
            colors: [
                '#0a6c5e', '#bb7918'
            ],
            areaOpacity: 0.7
        }
    };

    tui.chart.registerTheme('Ad_theme', theme_a);
    options_a.theme = 'Ad_theme';

    tui.chart.columnChart(container_a, data_a, options_a);


    var container_reg = document.getElementById('regret_chart');
    var data_reg = {
        categories: numberRange(1,1001),
        series: [
            {
                name: 'Random Sampling',
                data: data.regret_rs
            },
            {
                name: 'Epsilon Greedy',
                data: data.regret_eg
            },
            {
                name: 'Thompson Sampling',
                data: data.regret_ts
            },
            {
                name: 'UCB1',
                data: data.regret_ucb1
            }
        ]
    };
    var options_reg = {
        chart: {
            width: 1100,
            height: 450,
            title: 'Regret by the Algorithm'
        },
        yAxis: {
            title: 'Regret',
        },
        xAxis: {
            title: 'Trial #',
            pointOnColumn: true,
            tickInterval: 'auto'
        },
        series: {
            showDot: false,
            zoomable: true
        },
    };
     options_reg.theme = 'Reward_theme';
    var chart = tui.chart.lineChart(container_reg, data_reg, options_reg);

}