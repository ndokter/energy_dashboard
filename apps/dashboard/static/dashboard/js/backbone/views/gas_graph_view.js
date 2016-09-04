var app = app || {};


(function ($) {
	'use strict';

    app.GasGraphView = Backbone.View.extend({
        tagName: 'canvas',

        render: function(start, end, aggregation, dataType) {
            this.renderChart(start, end, aggregation, dataType);

            return this;
        },

        renderChart: function(start, end, aggregation, dataType) {
            let gasUsedCollection = new app.GasUsedCollection(start, end, aggregation),
                canvas = $(this.el);

            gasUsedCollection.fetch({
                success: function (gasUsedCollection, response) {
                    let dataLabels = [],
                        dataPoints = [],
                        data;

                    gasUsedCollection.each(function (item, index, all) {
                        dataLabels.push(moment.utc(item.attributes.datetime).local().format('HH:ss'));

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

                    new Chart(canvas, {
                        type: 'line',
                        data: data
                    });
                }
            });
        }
    });
})(jQuery);
