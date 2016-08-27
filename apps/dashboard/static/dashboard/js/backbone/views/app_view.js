var app = app || {};

(function ($) {
	'use strict';

	app.AppView = Backbone.View.extend({
        el: $('body'),

        initialize: function() {
             _.bindAll(this, 'render');

            this.electricityUsedView = new app.ElectricityGraphView();
            this.gasUsedView = new app.GasGraphView();

            this.render();
        },

		render: function () {
            $(this.el).append(
                this.electricityUsedView.render().el,
                this.gasUsedView.render().el
            );
		}
	});
})(jQuery);
