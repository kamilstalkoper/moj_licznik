/**
 * Created by piotrekzawada on 12.12.2016.
 */
$(function() {
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

});
