var app = app || {};

(function ($) {
	'use strict';

	app.DashboardView = Backbone.View.extend({
	    tagName: 'div',

        template: _.template($('#dashboard-template').html()),

        initialize: function() {
            this.electricityActualCollection = new app.ElectricityUsedActualCollection(
                moment('2017-03-18T18:56:13'),
                moment('2017-03-18T19:59:17'),
                'second',
                '-datetime',
                1
            );

            this.gasUsedTodayView = new app.GasGraphView();
            this.electricityTodayView = new app.ElectricityGraphView();

            this.render();
        },

		render: function () {

            // TODO this gets the current actual electricity used value
            this.electricityActualCollection.fetch({
                success: function (data, response) {
                    console.log(data);
                    data.each(function (item, index, all) {
                        console.log(item);
                        console.log(item.attributes.datetime, item.attributes.value);
                    });
                }
            });


    		this.$el.html(this.template({'test': 'testtt'}));

		    $('#graph-gas-today', this.$el).html(
                this.gasUsedTodayView.render(
                    moment('2017-03-19T00:00:00'),
                    moment('2017-03-20T00:00:00'),
                    'hour',
                    'usage'
                ).$el
		    )

		    $('#graph-electricity-today', this.$el).html(
                this.electricityTodayView.render(
                    moment('2017-03-19T00:00:00'),
                    moment('2017-03-20T00:00:00'),
                    'hour',
                    'usage'
                ).$el
		    )

            return this;
		}
	});
})(jQuery);
