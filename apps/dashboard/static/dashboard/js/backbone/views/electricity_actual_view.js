var app = app || {};


(function ($) {
	'use strict';

    app.ElectricityActualView = Backbone.View.extend({
        tagName: 'canvas',

        initialize: function() {
            this.chart = null;

            this.end = moment();
            this.start = moment().subtract(60, 'minutes');
        },

        render: function() {
            this.renderChart(this.start, this.end, 'second');

            return this;
        },

        renderChart: function(start, end, aggregation) {
            let electricityUsedCollection = new app.ElectricityUsedActualCollection(start, end, aggregation),
                canvas = $(this.el),
                dateFormat,
                that = this;

            this.$el.addClass('graph-loading');

            if (aggregation == 'hour') {
                dateFormat = 'HH:ss';
            } else if (aggregation == 'day') {
                dateFormat = 'ddd D MMM';
            } else if (aggregation == 'month') {
                dateFormat = 'MMMM YYYY';
            }

            electricityUsedCollection.fetch({
                success: function (electricityUsedCollection, response) {
                    let dataLabels = [],
                        dataPoints = [],
                        data;

                    electricityUsedCollection.each(function (item, index, all) {
                        dataLabels.push(moment.utc(item.attributes.datetime).local().format(dateFormat));


                            dataPoints.push(item.attributes.value * 1000);

                    });

                    data = {
                        labels: dataLabels,
                        datasets: [
                            {
                                backgroundColor: 'rgba(24,128,20,0.7)',
                                data: dataPoints
                            }
                        ]
                    };

                    if (that.chart !== null) {
                        that.chart.destroy();
                    }

                    that.chart = new Chart(canvas, {
                        type: 'bar',
                        data: data,
                        options: {
                            scales: {
                                yAxes: [{
                                    ticks: {
                                        beginAtZero:true
                                    }
                                }]
                            }
                        }
                    });

                    that.$el.removeClass('graph-loading');
                }
            });
        }
    });
})(jQuery);
