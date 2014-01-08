App.Collections.Earthquakes = Backbone.Collection.extend({
    model: App.Models.Earthquake,
    url: 'api/earthquake',
    parse: function(response){
        return response.objects;
    }
});