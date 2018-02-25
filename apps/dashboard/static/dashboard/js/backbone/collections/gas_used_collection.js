var app = app || {};


(function ($) {
	'use strict';

    app.GasUsedCollection = Backbone.Collection.extend({
        initialize: function(start, end, aggregation) {
            this.start = start;
            this.end = end;
            this.aggregation = aggregation;
        },

        url: function() {
            let start = this.start.utc().format('YYYY-MM-DD HH:mm:ss'),
                end = this.end.utc().format('YYYY-MM-DD HH:mm:ss');

            return '/api/metrics/gas/usage/total/' + this.aggregation + '/' + '?datetime_start=' + start + '&datetime_end=' + end;
        }
    });
})(jQuery);
