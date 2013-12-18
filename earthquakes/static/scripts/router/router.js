App.Router = Backbone.Router.extend({

    initialize: function(){
        /* initialize the collection to the application and
        fetch data here backbone docs says you shouldn't use
        fetch to populate collection on page load but my data
        is on a server and i don't know another way at this
        time need to refresh the collection when user navigates
        to the home page view */
        window.earthquakeCollection = new App.Collections.Earthquakes();
        window.earthquakeCollection.fetch({
            async: false,
        });
    },

    routes: {
        "": "listView",
        "earthquakes/:primary_id": "detailView"
    },

    listView: function(){

        // empty detail div when view is rendered
        // has to be a better way
        $("#earthquake-entry").empty();

        /* assign the window's collection to my list view
        and render it when user is on the 'home page' */
        this.listView = new App.Views.ListView({
            collection: window.earthquakeCollection
        });
        this.listView.render().el;
    },

    detailView: function(primary_id){

        // empty list div when view is rendered
        // has to be a better way
        $("#earthquake-entries").empty();

        /* find the model in the window's collection
        that matches the primary id and render the
        detail view using that model. This allows the
        user to 'bookmark' the detail view */
        this.model = window.earthquakeCollection.where({primary_id: parseInt(primary_id)});
        this.detailView = new App.Views.DetailView({
            model: this.model[0]
        });
        this.detailView.render().el;
    },

    loadView: function(view){
        this.view && this.view.remove();
        this.view = view;
    }
});