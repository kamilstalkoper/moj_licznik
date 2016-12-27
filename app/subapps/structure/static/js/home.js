/**
 * Created by piotrekzawada on 12.12.2016.
 */
$(function() {
    if($('.goal-wrapper').length){
        var opts = {
            lines: 12,
            angle: 0,
            lineWidth: 0.4,
            pointer: {
                length: 0.75,
                strokeWidth: 0.042,
                color: '#1D212A'
            },
            limitMax: 'false',
            colorStart: '#1ABC9C',
            colorStop: '#1ABC9C',
            strokeColor: '#F0F3F3',
            generateGradient: true
        };

        var target = document.getElementById('foo2'),
            gauge = new Gauge(target).setOptions(opts),
            maxValue= parseInt($('span.goal-value').text()),
            result = parseInt($('span.gauge-value').text());

        gauge.maxValue = maxValue;
        gauge.animationSpeed = 20;
        gauge.set(result);
        gauge.setTextField(document.getElementById("gauge-text2"));
    }

});
$(document).ready(function() {

    var cb = function(start, end, label) {
        console.log(start.toISOString(), end.toISOString(), label);
        $('#reportrange span').html(start.format('DD/MM/YYYY') + ' - ' + end.format('DD/MM/YYYY'));
    };

    var optionSet1 = {
        startDate: moment().subtract(29, 'days'),
        endDate: moment(),
        minDate: '01/01/2014',
        maxDate: '12/31/2017',
        dateLimit: {
            days: 60
        },
        showDropdowns: true,
        showWeekNumbers: true,
        timePicker: false,
        timePickerIncrement: 1,
        timePicker12Hour: true,
        ranges: {
            'Dziś': [moment(), moment()],
            'Wczoraj': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Ostatnie 7 dni': [moment().subtract(6, 'days'), moment()],
            'Ostatnie 30 dni': [moment().subtract(29, 'days'), moment()],
            'Ten miesiąc': [moment().startOf('month'), moment().endOf('month')],
            'Poprzedni miesiąc': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        },
        opens: 'left',
        buttonClasses: ['btn btn-default'],
        applyClass: 'btn-small btn-primary',
        cancelClass: 'btn-small',
        format: 'DD/MM/YYYY',
        separator: ' do ',
        locale: {
            applyLabel: 'Zatwierdź',
            cancelLabel: 'Wyczyść',
            fromLabel: 'Od',
            toLabel: 'Do',
            customRangeLabel: 'Custom',
            daysOfWeek: ['Ndz', 'Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sob'],
            monthNames: ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'],
            firstDay: 1
        }
    };
    $('#reportrange span').html(moment().subtract(29, 'days').format('DD/MM/YYYY') + ' - ' + moment().format('DD/MM/YYYY'));
    $('#reportrange').daterangepicker(optionSet1, cb);
    //$('#reportrange').on('show.daterangepicker', function() {
    //    console.log("show event fired");
    //});
    //$('#reportrange').on('hide.daterangepicker', function() {
    //    console.log("hide event fired");
    //});
    $('#reportrange').on('apply.daterangepicker', function(ev, picker) {
        //console.log("apply event fired, start/end dates are " + picker.startDate.format('MMMM D, YYYY') + " to " + picker.endDate.format('MMMM D, YYYY'));
    });
    //$('#reportrange').on('cancel.daterangepicker', function(ev, picker) {
    //    console.log("cancel event fired");
    //});
    $('#options1').click(function() {
        $('#reportrange').data('daterangepicker').setOptions(optionSet1, cb);
    });
    $('#options2').click(function() {
        $('#reportrange').data('daterangepicker').setOptions(optionSet2, cb);
    });
    $('#destroy').click(function() {
        $('#reportrange').data('daterangepicker').remove();
    });
});
$(document).ready(function() {
    if($("#placeholder33x").length){
        function drawNewChart(startDay, endDay) {
            //define chart clolors ( you maybe add more colors if you want or flot will add it automatic )
            var chartColours = ['#96CA59', '#3F97EB', '#72c380', '#6f7a8a', '#f7cb38', '#5a8022', '#2c7282'],
                days =parseInt((endDay-startDay)/86399999);

            //generate random number for charts
            randNum = function() {
                return (Math.floor(Math.random() * (1 + 40 - 10)));
            };

            var d1 = [];

            //here we generate data for chart from last_month array passed from buttom of home.html
            for (var i = 0; i < days+1; i++) {
                //new Date(Date.today().add(i).days()).getTime()
                d1.push([startDay+i*86399999, last_month[i]]);
                //d2.push([startDay+i*86399999, last_month[i]-randNum()]);
            }

            //console.log('d1', d1);

            var chartMinDate = d1[0][0]; //first day
            var chartMaxDate = d1[days][0]; //last day

            var tickSize = [1, "day"];
            var tformat = "%d/%m/%y";



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

            $("#placeholder33x").bind("plothover", function (event, pos, item) {
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

            var plot = $.plot($("#placeholder33x"), [{
                label: "Zużycie",
                data: d1,
                lines: {
                    fillColor: "rgba(150, 202, 89, 0.12)"
                }, //#96CA59 rgba(150, 202, 89, 0.42)
                points: {
                    fillColor: "#fff"
                }
            }], options);

        }
        var todayDate = new Date(),
            today = todayDate.setHours(23,59,59,59),
            sevenDaysAgo = +today-604800000;

        drawNewChart(sevenDaysAgo, today);


        $('#reportrange').on('apply.daterangepicker', function(ev, picker) {
            console.log("star/end " + picker.startDate + " to " + picker.endDate);
            var range = parseInt((picker.endDate-picker.startDate)/86399999);
            drawNewChart(picker.startDate, picker.endDate);
        });
    }
});
