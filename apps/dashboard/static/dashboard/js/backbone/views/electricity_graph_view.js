var app = app || {};


(function ($) {
	'use strict';

    app.ElectricityGraphView = Backbone.View.extend({
        tagName: 'canvas',

        initialize: function() {
            this.chart = null;
        },

        render: function(start, end, aggregation, dataType) {
            this.renderChart(start, end, aggregation, dataType);

            return this;
        },

        renderChart: function(start, end, aggregation, dataType) {
            let electricityUsedCollection = new app.ElectricityUsedCollection(start, end, aggregation),
                canvas = $(this.el),
                dateFormat,
                that = this;

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

                        if (dataType == 'costs') {
                            dataPoints.push(item.attributes.costs);
                        } else if (dataType == 'usage') {
                            dataPoints.push(item.attributes.value);
                        }
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
                        type: 'line',
                        data: data,
                    });
                }
            });
        }
    });
})(jQuery);
