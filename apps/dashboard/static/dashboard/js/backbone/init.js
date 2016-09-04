var app = app || {};

$(function () {
    'use strict';

    Chart.defaults.global.legend.display = false;
    Chart.defaults.global.animation = false;
    Chart.defaults.global.maintainAspectRatio = false;
    Chart.defaults.global.responsive = true;

    new app.AppView();
});
