var app = app || {};


(function ($) {
	'use strict';

    app.ElectricityUsedCollection = Backbone.Collection.extend({
        url: '/api/readings/electricity/used/hour/'
    });
})(jQuery);
