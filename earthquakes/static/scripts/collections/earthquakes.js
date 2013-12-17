App.Collections.Earthquakes = Backbone.Collection.extend({
    model: App.Models.Earthquake,
    url: 'api/earthquakes',
    parse: function(response){
        return response.objects;
    }
});