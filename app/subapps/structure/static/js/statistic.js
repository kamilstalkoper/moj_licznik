/**
 * Created by piotrekzawada on 23.12.2016.
 */
$(document).ready(function() {
    function drawNewChart(startDay, endDay, meter_data) {
        //define chart clolors ( you maybe add more colors if you want or flot will add it automatic )
        var chartColours = ['#96CA59', '#3F97EB', '#72c380', '#6f7a8a', '#f7cb38', '#5a8022', '#2c7282'],
            days =parseInt((endDay-startDay)/86399999);

        console.log('days', days);

        //generate random number for charts
        randNum = function() {
            return (Math.floor(Math.random() * (1 + 40 - 10)));
        };

        var d1 = [],
            d2 = [];

        if(days == 1) {
            console.log('days 1')
            for (var i = 0; i < 24; i++) {
                d1.push([startDay + i * 3600000, meter_data[i]]);

            }
            var tickSize = [1, "hour"];
            var tformat = "%H";

            var chartMinDate = d1[0][0]; //first day
            var chartMaxDate = d1[23][0]; //last day
        }else{
            console.log('else')
            for (var i = 0; i < days + 1; i++) {
                d1.push([startDay + i * 86399999, meter_data[i]]);

            }
            var tickSize = [1, "day"];
            var tformat = "%d/%m/%y";

            var chartMinDate = d1[0][0]; //first day
            var chartMaxDate = d1[days][0]; //last day
        }


        //graph options
        var options = {
            grid: {
                show: true,
                aboveData: true,
                color: "#3f3f3f",
                labelMargin: 10,
                axisMargin: 0,
                borderWidth: 0,
                borderColor: null,
                minBorderMargin: 5,
                clickable: true,
                hoverable: true,
                autoHighlight: true,
                mouseActiveRadius: 100
            },
            series: {
                lines: {
                    show: true,
                    fill: true,
                    lineWidth: 2,
                    steps: false
                },
                points: {
                    show: true,
                    radius: 4.5,
                    symbol: "circle",
                    lineWidth: 3.0
                }
            },
            legend: {
                position: "ne",
                margin: [0, -25],
                noColumns: 0,
                labelBoxBorderColor: null,
                labelFormatter: function(label, series) {
                    // just add some space to labes
                    return label + '&nbsp;&nbsp;';
                },
                width: 40,
                height: 1
            },
            colors: chartColours,
            shadowSize: 0,
            tooltip: true, //activate tooltip
            tooltipOpts: {
                content: "%s: %y.0",
                xDateFormat: "%d/%m",
                shifts: {
                    x: -30,
                    y: -50
                },
                defaultTheme: false
            },
            yaxis: {
                min: 0
            },
            xaxis: {
                mode: "time",
                minTickSize: tickSize,
                timeformat: tformat,
                min: chartMinDate,
                max: chartMaxDate
            }
        };

        $("<div id='tooltip'></div>").css({
            position: "absolute",
            display: "none",
            border: "1px solid #fdd",
            padding: "2px",
            "background-color": "#fee",
            opacity: 0.80
        }).appendTo("body");

        $("#placeholder1").bind("plothover", function (event, pos, item) {
            if (item) {
                var x = item.datapoint[0].toFixed(2),
                    y = item.datapoint[1].toFixed(2);

                $("#tooltip").html(y + ' kWh')
                    .css({top: item.pageY+5, left: item.pageX+5})
                    .fadeIn(200);
            } else {
                $("#tooltip").hide();
            }
        });

        var plot = $.plot($("#placeholder1"), [{
            label: "Zużycie",
            data: d1,
            lines: {
                fillColor: "rgba(150, 202, 89, 0.12)"
            }, //#96CA59 rgba(150, 202, 89, 0.42)
            points: {
                fillColor: "#fff"
            }
        }], options);

        $('#simulateEco').on('click', function(e){
            e.preventDefault();
            var powerSource = parseFloat($('#powerSource').val()),
                dayLenght = [
                    [8.425],
                    [9.95],
                    [11.93],
                    [13.975],
                    [15.7],
                    [16.575],
                    [16.1],
                    [14.55],
                    [12.6],
                    [10.6],
                    [8.825],
                    [7.95]
                ],
                powerProduced = 0,
                realSum = 0;

            for (var i = 0; i < days; i++) {
                var date = new Date(startDay+i*86399999);
                d2.push([startDay+i*86399999, powerSource*dayLenght[date.getMonth()]]);
                powerProduced += powerSource*dayLenght[date.getMonth()];
            }
            realSum = parseInt($('#yourSum').text()) - powerProduced;

            $('.ecoSum').removeClass('hidden');
            $('#producedSum').html(powerProduced.toFixed(2) + ' kWh');

            if(realSum > 0){
                $('#realSum').html(realSum.toFixed(2) + ' kWh');
            }else{
                $('#realSum').html(0 + ' kWh');
            }

            var plot = $.plot($("#placeholder1"), [{
                label: "Zużycie",
                data: d1,
                lines: {
                    fillColor: "rgba(150, 202, 89, 0.12)"
                }, //#96CA59 rgba(150, 202, 89, 0.42)
                points: {
                    fillColor: "#fff"
                }
            },
                {
                    label: "Produkcja",
                    data: d2,
                    lines: {
                        fillColor: "rgba(63, 151, 235, 0.12)"
                    }, //#96CA59 rgba(150, 202, 89, 0.42)
                    points: {
                        fillColor: "#fff"
                    }
                }], options);

        })

    }

    $('#reportrange').on('apply.daterangepicker', function(ev, picker) {
        //console.log("star/end " + picker.startDate.format('YYYY-MM-DD'), + " to " + picker.endDate.format('YYYY-MM-DD'));
        var range = parseInt((picker.endDate-picker.startDate)/86399999);
        var startDate = picker.startDate.format("YYYY-MM-DD"),
            endDate = picker.endDate.format("YYYY-MM-DD");

        console.log('range', range);

        console.log("star/end " + startDate.toString() + " to " + endDate.toString());

        $.ajax({
            url: '/zuzycie/api/get_meter_data',
            dataType: 'json',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
                'start_date': startDate.toString(),
                'end_date': endDate.toString()
            },
            success: function (data, status, xhr) {
                console.log(data)
                drawNewChart(picker.startDate, picker.endDate, data.meter_data);
                $('#yourSum').html(data.user_meter_data_sum + ' kWh');
                $('#neighborsSum').html(data.others_avg + ' kWh');
                $('#statisticTiles').show();
                if(range == 1){
                    $('.simulate-eco').hide();
                }
            },
            error: function (xhr, status, error) {
                console.log('Błąd: ', xhr.status)
            }
        })
    });
});