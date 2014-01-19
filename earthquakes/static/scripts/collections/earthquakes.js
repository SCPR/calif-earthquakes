App.Collections.Earthquakes = Backbone.Collection.extend({
    model: App.Models.Earthquake,
    url: SITE_RELATIVE_ROOT + '/api/earthquake?q={"order_by":[{"field":"date_time","direction":"desc"}]}',
    parse: function(response){
        return response.objects;
    }
});