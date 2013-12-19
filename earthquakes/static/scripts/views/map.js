App.Views.MapView = Backbone.View.extend({
    tagName: "div",

    id: 'content-map-canvas',

    className: "initial",

    initialize: function(markersCollectionObject){

        if (navigator.userAgent.match(/(iPad)|(iPhone)|(iPod)|(android)|(webOS)/i)) {
            this.initialZoom = 3;
        } else {
            this.initialZoom = 6;
        }

        this.center = new L.LatLng(36.750439,-119.77237);

        this.stamenToner = L.tileLayer('http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png', {
            attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
        	subdomains: 'abcd',
        });

        this.mapQuest = L.tileLayer('http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {
            attribution: 'Tiles, data, imagery and map information provided by <a href="http://www.mapquest.com" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png">, <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and OpenStreetMap contributors.',
            subdomains: ['otile1','otile2','otile3','otile4']
        });

        this.render(markersCollectionObject);
    },

    render: function(markersCollectionObject){

        $(this.el).insertBefore("#earthquake-entries-container");
        var map = this.map = L.map('content-map-canvas', {
            scrollWheelZoom: false,
            zoomControl: true
        }).addLayer(
            this.stamenToner
        ).setView(
            this.center, this.initialZoom
        );

        this.markersObject = markersCollectionObject.model.attributes;
        this.markersObject.map = map;
        this.markerViews = new App.Views.ClusteredMarkerView(this.markersObject);

        //this.markerViews = this.model.get('markers').map(function(marker){
            //return new App.Views.MarkerView({model: marker, map: map}).render();
        //});

    }
});