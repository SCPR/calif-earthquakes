App.Collections.LaHabraEarthquakes = Backbone.Collection.extend({
    model: App.Models.Earthquake,
    url: '/earthquaketracker/api/v1.0/earthquakes/la-habra-quakes',
    parse: function(response){
        return response.objects;
    }
});