var app = app || {};

(function ($) {
	'use strict';

	app.AppView = Backbone.View.extend({
        el: 'body',
        template: _.template($('#index-template').html()),

        // TODO: use url routing, this was a quickfix
        events: {
            'click #home'       : 'renderDashboard',
            'click #reports'    : 'renderReports',
        },

        initialize: function() {
//            this.dashboardView = new app.DashboardView();
//            this.reportView = new app.ReportView();

            this.render();
        },

        renderDashboard: function(e) {
            $('#body', this.$el).html(new app.DashboardView().el);
        },

        renderReports: function(e) {
            $('#body', this.$el).html(new app.ReportView().el);
        },

		render: function () {
		    this.$el.html(this.template());
//		    this.renderDashboard();
//		    this.renderReports();

            //tmp
            $('#body', this.$el).append(new app.ReportView().el);
//            $('#body', this.$el).append(new app.ElectricityActualView().el);

            $('#body', this.$el).append(
                $('<div/>').addClass('canvas-wrapper').append(
                    new app.ElectricityActualView().render().$el
                )
            );


		    return this;
		}
	});
})(jQuery);
