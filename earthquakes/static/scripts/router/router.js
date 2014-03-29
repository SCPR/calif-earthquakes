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
        "explore-the-map": "fullScreenView",
        "la-habra-earthquakes": "laHabraQuakeMap",
    },

    laHabraQuakeMap: function(){
        var mapContainer = ".content-map-container";
        this.laHabraMap(mapContainer, window.earthquakeCollection, 'static/templates/la-habra-earthquakes.html', 13);
    },

    fullScreenView: function(){
        var mapContainer = ".content-map-container";
        this.createMap(mapContainer, window.earthquakeCollection, 'static/templates/map-full-view.html', 7);
    },

    indexView: function(){
        var mapContainer = ".content-map-container";
        this.createMap(mapContainer, window.earthquakeCollection, 'static/templates/map-index-view.html', 6);
    },

    createMap: function(mapContainer, markers, template, initialZoom){
        // if mapView on page remove it

        if (this.mapView){
            this.mapView.remove();
        };

        this.mapModel = new App.Models.Map({
            markers: markers
        });

        this.mapView = new App.Views.MapView({
            model: this.mapModel,
            container: mapContainer,
            template: template,
            initialZoom: initialZoom
        });

        return this.mapView;
    },

    laHabraMap: function(mapContainer, markers, template, initialZoom){
        // if mapView on page remove it

        if (this.mapView){
            this.mapView.remove();
        };

        this.mapModel = new App.Models.Map({
            markers: markers
        });

        this.mapView = new App.Views.LaHabraView({
            model: this.mapModel,
            container: mapContainer,
            template: template,
            initialZoom: initialZoom
        });

        return this.mapView;
    }

});