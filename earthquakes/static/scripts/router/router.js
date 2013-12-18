App.Router = Backbone.Router.extend({

    initialize: function(){

        // create instance of our collection
        this.earthquakeCollection = new App.Collections.Earthquakes();

        // fetch data to add to our collection
        this.earthquakeCollection.fetch({
            async: false,
        });

        // create instance of our items view
        this.earthquakeList = new App.Views.ListView({
            collection: this.earthquakeCollection
        });

        // render the items view
        this.earthquakeList.render().el;

    },

    routes: {
        "": "home",
        "earthquakes/:primary_id": "earthquakes"
    },

    home: function(){
        console.log('home');
        $("#earthquake-entry").empty();
        this.initialize();
    },

    earthquakes: function(primary_id){
        $("#earthquake-entries").empty();


        // where the work has to happen
        this.model = this.earthquakeCollection.where({primary_id: parseInt(primary_id)});
        var newDetail = new App.Views.DetailView({
            model: this.model.attributes
        });


    },

    loadView: function(view){
        this.view && this.view.remove();
        this.view = view;
    }
});