var app = app || {};

(function ($) {
	'use strict';

	app.ReportView = Backbone.View.extend({
	    tagName: 'div',

        template: _.template($('#report-graph-wrapper-template').html()),

        initialize: function() {
            this.period = 'hours';
            this.aggregation = 'hour';
            this.dataType = 'costs'

            this.start = moment().startOf('day');
            this.end = moment(this.start).endOf('day');

            this.electricityUsedView = new app.ElectricityGraphView();
            this.gasUsedView = new app.GasGraphView();

            this.render();
        },

        events: {
            'click .date-period button'    : 'changePeriod',
            'click .next-date'             : 'nextDate',
            'click .previous-date'         : 'previousDate',
            'click .data-type button'      : 'changeDataType',
        },

        changePeriod: function(e) {
            let target = $(e.target, this.$el);

            this.period = target.data('period')

            // Redetermine what button is highlighted as 'active'.
            $('.date-period button', this.$el).removeClass('active');
            target.addClass('active');

            if (this.period == 'hours') {
                this.start = moment().local().startOf('day');
                this.end = moment(this.start).endOf('day');
                this.aggregation = 'hour';
            } else if (this.period == 'days') {
                this.start = moment().local().startOf('month');
                this.end = moment(this.start).endOf('month');
                this.aggregation = 'day';
            } else if (this.period == 'months') {
                this.start = moment().local().startOf('year');
                this.end = moment(this.start).endOf('year');
                this.aggregation = 'month';
            }

            this.renderCurrentDate();
            this.renderGraphs();
        },

        nextDate: function() {
            if (this.period == 'hours') {
                this.start.local().add(1, 'day');
                this.end = this.start.clone().endOf('day');
            } else if (this.period == 'days') {
                this.start.local().add(1, 'month');
                this.end = this.start.clone().endOf('month');
            } else if (this.period == 'months') {
                this.start.local().add(1, 'year');
                this.end = this.start.clone().endOf('year');
            }

            this.renderCurrentDate();
            this.renderGraphs();
        },

        previousDate: function() {
            if (this.period == 'hours') {
                this.start.local().subtract(1, 'day');
                this.end = moment(this.start).endOf('day');
            } else if (this.period == 'days') {
                this.start.local().subtract(1, 'month');
                this.end = moment(this.start).endOf('month');
            } else if (this.period == 'months') {
                this.start.local().subtract(1, 'year');
                this.end = moment(this.start).endOf('year');
            }

            this.renderCurrentDate();
            this.renderGraphs();
        },

        changeDataType: function(e) {
            let target = $(e.target, this.$el);

            this.dataType = target.data('type')

            // Redetermine what button is highlighted as 'active'.
            $('.data-type button', this.$el).removeClass('active');
            target.addClass('active');

            this.renderCurrentDate();
            this.renderGraphs();
        },


		render: function () {
		    this.$el.html(this.template());

            this.renderCurrentDate();
            this.renderGraphs();

            return this;
		},

        renderCurrentDate: function() {
            let date = '';

            if (this.period == 'hours') {
                date = this.start.local().format('D MMMM');
            } else if (this.period == 'days') {
                date = this.start.local().format('MMMM YYYY');
            } else if (this.period == 'months') {
                date = this.start.local().format('YYYY');
            }

            $('.current-date', this.$el).html(date);
        },

		renderGraphs: function() {
		    let panelBody = $(".panel-body", this.$el);

		    panelBody.empty();

		    // Wrap the canvas'es in a div which determines the chart size. This
		    // is due to some difficulties with ChartJS:
		    // https://github.com/chartjs/Chart.js/issues/56
		    panelBody.append(
                $('<div/>').addClass('canvas-wrapper').append(
                    this.electricityUsedView.render(
                        this.start,
                        this.end,
                        this.aggregation,
                        this.dataType
                    ).$el
                )
            );

            panelBody.append(
                $('<div/>').addClass('canvas-wrapper').append(
                    this.gasUsedView.render(
                        this.start,
                        this.end,
                        this.aggregation,
                        this.dataType
                    ).$el
                )
            );
		}
	});
})(jQuery);
