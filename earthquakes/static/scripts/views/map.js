App.Views.MapView = Backbone.View.extend({
    template: _.template(template("static/templates/full-screen-map.html")),

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

        this.CaliforniaFaults = L.imageOverlay('http://www.lib.utexas.edu/maps/historical/newark_nj_1922.jpg',
            imageBounds = [
                [40.712216, -74.22655],
                [40.773941, -74.12544]
            ]);
        */

        /*
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
        */


        if (navigator.userAgent.match(/(iPad)|(iPhone)|(iPod)|(android)|(webOS)/i)) {
            this.initialZoom = 3;
        } else {
            this.initialZoom = 7;
        }

        this.center = new L.LatLng(37.335194502529724, -119.366455078125);
        this.render(markersCollection);
    },

    events: {
        // hits the navigate function when the submit button is pressed
        "click button#submit": "navigate",

        // triggers address search funtion when key input
        "keyup :input": "addressSearch",

        // triggers geolocation when anchor tag clicked
        "click a.findMe": "findMe",

        // triggers search me
        "click a.searchMe": "searchMe",

        // used to toggle layers
        "click [type='checkbox']": "toggleLayers",
    },

    // adds lat and lng to form fields
    // retrieve values when enter pressed
    addressSearch: function(e){
        $("input[id='addressSearch']").focus(function(){
            console.log('key input');
        });

        $("input[id='addressSearch']").geocomplete({
            details: "form"
        });

        var latitude = $("input[id='latitudeSearch']").val();
        var longitude = $("input[id='longitudeSearch']").val();

    	if(e.keyCode != 13) {
    	    return false;
    	} else if (e.keyCode === 13 && latitude === '' && longitude === '') {
    	    return false;
    	} else {
            this.navigate();
    	}
    },


    findMe: function(){
        console.log('find me');
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                $("input[id='latitudeSearch']").val(position.coords.latitude);
                $("input[id='longitudeSearch']").val(position.coords.longitude);
                $("button#submit").trigger("click");
            }, null);
        } else {
            alert("Sorry, we could not find your location.");
        }
    },

    searchMe: function(){
        console.log('search me');
    },


    navigate: function(){
        var latitude = $("input[id='latitudeSearch']").val();
        var longitude = $("input[id='longitudeSearch']").val();

        if (latitude === '' && longitude === ''){
            alert('nothing there')

        } else {
            var locationParams = latitude + ", " + longitude;
            this.userLocationCenter = new L.LatLng(latitude, longitude);
            this.userLocationMarker = L.marker([latitude, longitude]).addTo(this.map);
            this.map.setView(this.userLocationCenter, 12);

            this.userRadius = L.circle([latitude, longitude], 805, {
                opacity: 0.5,
                weight: 2,
                color: '#4b58a6',
                fillColor: '#4b58a6',
                fillOpacity: 0.5
            }).addTo(this.map);

        }
    },






    toggleLayers: function(event){

        console.log('toggle me');
        /*
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
        */

    },

    render: function(markersCollection){
        //$(markersCollection.container).html(this.$el.html(this.template()));

        $(markersCollection.container).html(this.$el.html(this.template()));

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

        //this.model = markersCollection.model.attributes;
        //this.model.map = this.map;
        //this.markerViews = new App.Views.ClusteredMarkerView(this.model);

        //this.markerViews = this.model.get('markers').map(function(marker){
            //return new App.Views.MarkerView({model: marker, map: map}).render();
        //});

    }
});