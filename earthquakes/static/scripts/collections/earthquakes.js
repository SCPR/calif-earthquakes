App.Collections.Earthquakes = Backbone.Collection.extend({
    model: App.Models.Earthquake,
    url: SITE_RELATIVE_ROOT + 'api/earthquake',
    parse: function(response){
        return response.objects;
    }
});