App.Views.MapView = Backbone.View.extend({
    tagName: "section",

    className: "dashboard clearfix",

    template: _.template(template("static/templates/map-view.html")),

    initialize: function(markersCollection){

        this.stamenToner = L.tileLayer("http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png", {
            attribution: "Map tiles by <a href='http://stamen.com' target='_blank'>Stamen Design</a>, <a href='http://creativecommons.org/licenses/by/3.0' target='_blank'>CC BY 3.0</a> &mdash; Map data &copy; <a href='http://openstreetmap.org' target='_blank'>OpenStreetMap</a> contributors, <a href='http://creativecommons.org/licenses/by-sa/2.0/' target='_blank'>CC-BY-SA</a>",
        	subdomains: "abcd",
        	minZoom: 0,
        	maxZoom: 17
        });

        this.mapQuest = L.tileLayer("http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png", {
            attribution: "Tiles, data, imagery and map information provided by <a href='http://www.mapquest.com' target='_blank'>MapQuest</a> <img src='http://developer.mapquest.com/content/osm/mq_logo.png'>, <a href='http://www.openstreetmap.org/' target='_blank'>OpenStreetMap</a> and OpenStreetMap contributors.",
            subdomains: ["otile1","otile2","otile3","otile4"]
        });

        /*
        this.CaliforniaFaults = new L.Shapefile('static/data/quaternary-faults/fault-areas.zip', {
            style: function (feature) {
                return {
                    color: 'green',
                    weight: 2,
                    opacity: 1,
                    fillColor: null,
                    fillOpacity: 0
                }
            },
        });
        */

        this.CaliforniaFaults = L.imageOverlay('http://www.lib.utexas.edu/maps/historical/newark_nj_1922.jpg',
            imageBounds = [
                [40.712216, -74.22655],
                [40.773941, -74.12544]
            ]);

        this.CaliforniaBoundaries = new L.Shapefile('static/data/california/california-counties.zip', {
            style: function (feature) {
                return {
                    color: '#787878',
                    weight: 2,
                    opacity: 1,
                    fillColor: null,
                    fillOpacity: 0
                }
            }
        });

        if (navigator.userAgent.match(/(iPad)|(iPhone)|(iPod)|(android)|(webOS)/i)) {
            this.initialZoom = 3;
        } else {
            this.initialZoom = 6;
        }

        this.center = new L.LatLng(34.257216,-118.131351);
        this.render(markersCollection);
    },

    events: {
        "click [type='checkbox']": "toggleLayers",
    },

    toggleLayers: function(event){

        if ($('#fault-lines').is(":checked")){
            this.map.addLayer(this.CaliforniaFaults);
            $("#fault-lines").attr("value", "shown");
            $("label[for='fault-lines']").text("Hide fault lines");
        } else {
            this.map.removeLayer(this.CaliforniaFaults);
            $("#fault-lines").attr("value", "hidden");
            $("label[for='fault-lines']").text("Show fault lines");
        };

        if ($('#county-boundaries').is(":checked")){
            this.map.addLayer(this.CaliforniaBoundaries);
            $("#county-boundaries").attr("value", "shown");
            $("label[for='county-boundaries']").text("Hide county boundaries");
        } else {
            this.map.removeLayer(this.CaliforniaBoundaries);
            $("#county-boundaries").attr("value", "hidden");
            $("label[for='county-boundaries']").text("Show county boundaries");
        };
    },

    render: function(markersCollection){

        console.log(markersCollection);

        $(this.$el.html(this.template())).insertAfter("section.latest");

        $("#slider").rangeSlider({
            defaultValues: {min: 1.5, max: 3.5},
            bounds: {min: 1, max: 5},
            step: .1
        }).bind("valuesChanging", function(e, data){
            console.log("Something moved. min: " + data.values.min + " max: " + data.values.max);
        });

        var mapOverlays = {
            "Counties": this.laCounty,
            "Faults": this.CaliforniaFaults
        };

        this.map = L.map("content-map-canvas", {
            scrollWheelZoom: false,
            zoomControl: true
        }).setView(
            this.center, this.initialZoom
        ).addLayer(
            this.stamenToner
        );

        //this.shpfile.addTo(this.map);
        //L.control.layers(null, mapOverlays).addTo(map);

        this.model = markersCollection.model.attributes;
        this.model.map = this.map;
        this.markerViews = new App.Views.ClusteredMarkerView(this.model);

        //this.markerViews = this.model.get('markers').map(function(marker){
            //return new App.Views.MarkerView({model: marker, map: map}).render();
        //});

    }
});