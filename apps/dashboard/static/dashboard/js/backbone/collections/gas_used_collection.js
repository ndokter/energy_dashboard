var app = app || {};


(function ($) {
	'use strict';

    app.GasUsedCollection = Backbone.Collection.extend({
        url: '/api/readings/gas/used/hour/'
    });
})(jQuery);
