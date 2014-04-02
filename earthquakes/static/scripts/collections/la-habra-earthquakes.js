App.Collections.Earthquakes = Backbone.Collection.extend({
    model: App.Models.Earthquake,
    url: SITE_RELATIVE_ROOT + '/earthquaketracker/api/v1.0/earthquakes',
    parse: function(response){
        return response.objects;
    }
});