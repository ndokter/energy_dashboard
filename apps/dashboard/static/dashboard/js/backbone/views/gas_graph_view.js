var app = app || {};


(function ($) {
	'use strict';

    app.GasGraphView = Backbone.View.extend({
        tagName: 'canvas',

        initialize: function() {
            this.chart = null;
        },

        render: function(start, end, aggregation, dataType) {
            this.renderChart(start, end, aggregation, dataType);

            return this;
        },

        renderChart: function(start, end, aggregation, dataType) {
            let gasUsedCollection = new app.GasUsedCollection(start, end, aggregation),
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

            gasUsedCollection.fetch({
                success: function (gasUsedCollection, response) {
                    let dataLabels = [],
                        dataPoints = [],
                        data;

                    gasUsedCollection.each(function (item, index, all) {
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
                                backgroundColor: 'rgba(209,25,50,0.7)',
                                data: dataPoints
                            }
                        ]
                    };

                    if (that.chart !== null) {
                        that.chart.destroy();
                    }

                    that.chart = new Chart(canvas, {
                        type: 'bar',
                        options: {
                            scales: {
                                yAxes: [{
                                    ticks: {
                                        beginAtZero:true
                                    }
                                }]
                            }
                        },
                        data: data
                    });

                    that.$el.removeClass('graph-loading');
                }
            });
        }
    });
})(jQuery);
