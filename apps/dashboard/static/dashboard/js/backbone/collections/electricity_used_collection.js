var app = app || {};


(function ($) {
	'use strict';

    app.ElectricityUsedCollection = Backbone.Collection.extend({
        url: 'http://localhost:8000/api/readings/electricity/used/hour/'
    });
})(jQuery);
