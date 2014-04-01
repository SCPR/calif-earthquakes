App.Collections.Earthquakes = Backbone.Collection.extend({
    model: App.Models.Earthquake,
    url: SITE_RELATIVE_ROOT + '/api/earthquake?q={"filters":[{"name":"date_time_raw","op":"gte","val":"1396048252200"},{"name":"date_time_raw","op":"lte","val":"1396224744200"}],"order_by":[{"field":"date_time_raw","direction":"desc"}]}',
    parse: function(response){
        return response.objects;
    }
});