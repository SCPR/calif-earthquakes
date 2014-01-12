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
        "": "indexView",
        "full-screen-map": "fullScreenView",
    },

    fullScreenView: function(){
        console.log('fullScreenView');
        var mapContainer = ".content-map-container";
        this.createMap(mapContainer, window.earthquakeCollection);
    },

    indexView: function(){
        console.log('indexView');
        var mapContainer = ".content-map-container";
        this.createMap(mapContainer, window.earthquakeCollection, 'static/templates/full-screen-map.html');
    },

    createMap: function(mapContainer, markers, template){
        // if mapView on page remove it

        if (this.mapView){
            this.mapView.remove();
        };

        this.mapModel = new App.Models.Map({
            markers: markers
        });

        //console.log(this.mapModel);

        this.mapView = new App.Views.MapView({
            model: this.mapModel,
            container: mapContainer,
            template: template
        });

        console.log(this.mapView);
        return this.mapView;

    }
});