var app = app || {};


(function ($) {
	'use strict';

    app.ElectricityGraphView = Backbone.View.extend({
        template: _.template($('#energy-graph-template').html()),

        render: function() {
            this.$el.html(this.template({'title': 'Electriciteitsverbruik'}));

            this.renderChart();

            return this;
        },

        renderChart: function() {
            let electricityUsedCollection = new app.ElectricityUsedCollection(),
                canvas = $('canvas', this.el);

            electricityUsedCollection.fetch({
                success: function (electricityUsedCollection, response) {
                    let dataLabels = [],
                        dataPoints = [],
                        data;

                    electricityUsedCollection.each(function (item, index, all) {
                        dataLabels.push(moment.utc(item.attributes.datetime).local().format('HH:ss'));
                        dataPoints.push(item.attributes.costs);
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

                    new Chart(canvas, {
                        type: 'line',
                        data: data
                    });
                }
            });
        }
    });
})(jQuery);
