var app = app || {};


(function ($) {
	'use strict';

    app.GasGraphView = Backbone.View.extend({
        template: _.template($('#energy-graph-template').html()),

        render: function() {
            this.$el.html(this.template({'title': 'Gasverbruik'}));

            this.renderChart();

            return this;
        },

        renderChart: function() {
            let gasUsedCollection = new app.GasUsedCollection(),
                canvas = $('canvas', this.el);

            gasUsedCollection.fetch({
                success: function (gasUsedCollection, response) {
                    let dataLabels = [],
                        dataPoints = [],
                        data;

                    gasUsedCollection.each(function (item, index, all) {
                        dataLabels.push(moment.utc(item.attributes.datetime).local().format('HH:ss'));
                        dataPoints.push(item.attributes.costs);
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
