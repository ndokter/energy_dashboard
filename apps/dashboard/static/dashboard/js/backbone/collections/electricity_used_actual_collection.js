var app = app || {};


(function ($) {
	'use strict';

    app.ElectricityUsedActualCollection = Backbone.Collection.extend({
        initialize: function(start, end, aggregation, ordering, limit) {
            this.start = start;
            this.end = end;
            this.aggregation = aggregation;
            this.ordering = ordering;
            this.limit = limit;
        },

        url: function() {
            let start = this.start.utc().format('YYYY-MM-DD HH:mm:ss'),
                end = this.end.utc().format('YYYY-MM-DD HH:mm:ss'),
                url;

            // TODO Figure out proper way to apply filtering, ordering and limiting
            url = '/api/readings/electricity/usage/actual/' + this.aggregation + '/' + '?datetime_start=' + start + '&datetime_end=' + end;

            if (this.ordering) {
                url += '&ordering=' + this.ordering;
            }

            if (this.limit) {
                url += '&limit=' + this.limit;
            }

            return url;
        }
    });
})(jQuery);
