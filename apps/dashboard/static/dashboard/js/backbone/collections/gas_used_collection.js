var app = app || {};


(function ($) {
	'use strict';

    app.GasUsedCollection = Backbone.Collection.extend({
        url: 'http://localhost:8000/api/readings/gas/used/hour/'
    });
})(jQuery);
