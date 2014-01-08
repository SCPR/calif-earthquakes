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
        "earthquakes/:id": "detailView"
    },

    listView: function(){
        /* assign the window's collection to my list view
        and render it when user is on the 'home page' */

        this.loadView(new App.Views.ListView({
            collection: window.earthquakeCollection
        }));

        this.createMap(window.earthquakeCollection);
    },

    detailView: function(id){
        /* find the model in the window's collection
        that matches the primary id and render the
        detail view using that model. This allows the
        user to 'bookmark' the detail view */
        this.model = window.earthquakeCollection.where({id: parseInt(id)});

        this.loadView(new App.Views.DetailView({
            model: this.model[0]
        }));

        this.createMap(this.model);
    },

    createMap: function(markers){
        // if the mapView is on the page
        // remove it from the page

        if (this.mapView){
            this.mapView.remove();
        };

        this.mapModel = new App.Models.Map({
            markers: markers
        });

        //console.log(this.mapModel);

        this.mapView = new App.Views.MapView({
            model: this.mapModel
        });

        return this.mapView;

    },

    loadView: function(view){
        /* remove a view when it's no longer needed */
        this.view && (this.view.close ? this.view.close() : this.view.remove());
        this.view = view;
        $(".magnitude-log").append(this.view.render().el);
    }
});