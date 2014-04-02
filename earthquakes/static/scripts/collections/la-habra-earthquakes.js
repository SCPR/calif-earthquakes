App.Collections.LaHabraEarthquakes = Backbone.Collection.extend({
    model: App.Models.Earthquake,
    url: SITE_RELATIVE_ROOT + '/earthquaketracker/api/v1.0/earthquakes/la-habra-quakes',
    parse: function(response){
        return response.objects;
    }
});