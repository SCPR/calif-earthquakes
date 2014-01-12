App.Views.MapView = Backbone.View.extend({
    template: _.template(template("static/templates/full-screen-map.html")),

    initialize: function(markersCollection){

        this.stamenToner = L.tileLayer("http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png", {
            attribution: "Map tiles by <a href='http://stamen.com' target='_blank'>Stamen Design</a>, <a href='http://creativecommons.org/licenses/by/3.0' target='_blank'>CC BY 3.0</a> &mdash; Map data &copy; <a href='http://openstreetmap.org' target='_blank'>OpenStreetMap</a> contributors, <a href='http://creativecommons.org/licenses/by-sa/2.0/' target='_blank'>CC-BY-SA</a>",
        	subdomains: "abcd",
        	minZoom: 0,
        	maxZoom: 17
        });

        /*
        this.CaliforniaFaultLines = new L.Shapefile('static/data/quaternary-faults/fault-areas.zip', {
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

        this.CaliforniaCountyBoundaries = L.geoJson(californiaCounties, {
            style: function (feature) {
                return {
                    color: '#787878',
                    weight: 2,
                    opacity: 1,
                    fillColor: null,
                    fillOpacity: 0
                }
            },
            onEachFeature: function(feature, layer) {
                layer.on('click', function (e) {
                    console.log(feature.properties.NAMELSAD10 + ' county layer clicked');
                });
            }
        });

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
        //"click a.searchMe": "searchMe",

        // changes radius value
        "change #search-radius": "navigate",

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

    /*
    searchMe: function(){
        console.log('search me');
    },
    */

    navigate: function(){
        var latitude = $("input[id='latitudeSearch']").val();
        var longitude = $("input[id='longitudeSearch']").val();
        var searchRadius = $("select[id='search-radius']").val();
        if (latitude === '' && longitude === ''){
            alert('Please enter an address or search by location')
        } else {
            if (this.map.hasLayer(this.userLayer)){
                this.map.removeLayer(this.userLayer);
                this.addUserLayerToMap(latitude, longitude, searchRadius);
            } else {
                this.addUserLayerToMap(latitude, longitude, searchRadius);
            }
        }
    },

    addUserLayerToMap: function(latitude, longitude, searchRadius){

        // create our user layers
        this.userLocationCenter = new L.LatLng(latitude, longitude);
        this.userLocationMarker = L.marker([latitude, longitude]);
        this.userRadius = L.circle([latitude, longitude], searchRadius, {
            clickable: false,
            opacity: 0.3,
            weight: 1,
            color: '#ec792b',
            fillColor: '#ec792b',
            fillOpacity: 0.3
        });

        // add our user layers
        this.userLayer = new L.layerGroup();
        this.userLayer.addLayer(this.userLocationMarker).addLayer(this.userRadius);
        this.userLayer.addTo(this.map);

        // pan map to user layer and sets to radius of user
        this.map.fitBounds(this.userRadius.getBounds());

    },

    toggleLayers: function(event){

        console.log('toggle me');


        /*
        if ($('#fault-lines').is(":checked")){
            this.map.addLayer(this.CaliforniaFaultLines);
            $("#fault-lines").attr("value", "shown");
            $("label[for='fault-lines']").text("Hide fault lines");
        } else {
            this.map.removeLayer(this.CaliforniaFaultLines);
            $("#fault-lines").attr("value", "hidden");
            $("label[for='fault-lines']").text("Show fault lines");
        };
        */

        if ($('#county-boundaries').is(":checked")){
            this.map.addLayer(this.CaliforniaCountyBoundaries);
            $("#county-boundaries").attr("value", "shown");
            $("label[for='county-boundaries']").text("Hide county boundaries");
        } else {
            this.map.removeLayer(this.CaliforniaCountyBoundaries);
            $("#county-boundaries").attr("value", "hidden");
            $("label[for='county-boundaries']").text("Show county boundaries");
        };
    },

    render: function(markersCollection){
        $(markersCollection.container).html(this.$el.html(this.template()));

        $("#slider").rangeSlider({
            defaultValues: {min: 1.5, max: 3.5},
            bounds: {min: 1, max: 5},
            step: .1
        }).bind("valuesChanging", function(e, data){
            console.log("Something moved. min: " + data.values.min + " max: " + data.values.max);
        });

        this.map = L.map("content-map-canvas", {
            scrollWheelZoom: false,
            zoomControl: true
        }).setView(
            this.center, this.initialZoom
        ).addLayer(
            this.stamenToner
        );

        this.model = markersCollection.model.attributes;
        this.model.map = this.map;
        this.markerViews = new App.Views.ClusteredMarkerView(this.model);
    }
});