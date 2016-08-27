var app = app || {};

$(function () {
    'use strict';

    Chart.defaults.global.legend.display = false;
    Chart.defaults.global.animation.duration = 0;

    new app.AppView();
});
