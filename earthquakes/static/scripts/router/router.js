App.Router = Backbone.Router.extend({
    routes: {
        "": "index",
        "earthquakes/:primary_id": "searchEarthquakes"
    },

    searchEarthquakes: function(primary_id){
        primary_id = parseInt(primary_id);
        this.model = window.InitializePage.earthquakeCollection.where({'primary_id': primary_id});
        this.DetailView = new App.Views.DetailView({model: this.model});
    }
});