App.Router = Backbone.Router.extend({
    routes: {
        "": "home",
        "earthquakes/:primary_id": "earthquakes"
    },

    home: function(){
        $("#earthquake-entry").empty();
        this.loadView(new App.Views.Initialize());
    },

    earthquakes: function(primary_id){
        $("#earthquake-entries").empty();
    },

    loadView: function(view){
        this.view && this.view.remove();
        this.view = view;
    }
});