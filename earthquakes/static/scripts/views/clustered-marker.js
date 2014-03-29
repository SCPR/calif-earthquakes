App.Views.ClusteredMarkerView = Backbone.View.extend({

    initialize: function(markersCollection) {
        // create this.collection
        this.collection = markersCollection;

        $("#quantity").html(this.collection.markers.length);

        // create this.map
        this.map = this.collection.map;

        if (this.collection.markers.length === undefined || this.collection.markers.length === null){
            console.log('undefined length');
        } else if (this.collection.markers.length === 1){
            this.model = this.collection.markers[0].attributes;
            this.marker = L.marker([this.model.latitude, this.model.longitude]).addTo(this.map);
            this.bindEvent(this.marker, this.model);
        } else {
            this.addCollectionToMap(this.collection.markers.models);
        }
    },

    addCollectionToMap: function(arrayOfModels){
        var myIcon = L.Icon.extend({
            iconUrl: 'static/i/leaflet/blue-earthquake-pin-small.png',
            iconSize: [38, 95],
            iconAnchor: [22, 94],
            popupAnchor: [-3, -76]
        });

        this.markerCluster = L.markerClusterGroup({
            disableClusteringAtZoom: 16,
            zoomToBoundsOnClick: true,
            showCoverageOnHover: false
        });

        for(var i=0; i<arrayOfModels.length; i++){
            this.marker = L.marker([arrayOfModels[i].attributes.latitude, arrayOfModels[i].attributes.longitude],
                {icon: new myIcon({iconUrl: 'static/i/leaflet/blue-earthquake-pin-small.png'})});
            this.bindEvent(this.marker, arrayOfModels[i].attributes);
            this.markerCluster.addLayer(this.marker);
        };

        this.map.addLayer(this.markerCluster);
    },

    bindEvent: function(marker, attributes){
        marker.on("click", function(){
            marker.bindPopup(
                "<div class='map-marker'>"+
                    "<article>" +
                        "<a href='" + attributes.earthquake_tracker_url + "'>" +
                            "<h1>" + moment(attributes.pacific_timezone).format('MMMM D, YYYY, h:mm a') + "</h1>" +
                            "<ul>" +
                                "<li class='near'><strong>Location</strong>: " + attributes.place + "</li>" +
                            "</ul>" +
                            "<aside class='magnitude'><strong>Magnitude</strong>: " + attributes.mag + "</aside>" +
                        "</a>" +
                    "</article>" +
                "</div");
        }).openPopup();

        /*
        marker.on('click', function(){
            var html = _.template(template("static/templates/details-full-view.html"), attributes);
            $(".data-display").html(html);
        });
        */
    }
});

App.Views.SingleMarkerView = Backbone.View.extend({
    initialize: function(markersCollection) {

        // create this.collection
        this.collection = markersCollection;

        // create this.map
        this.map = this.collection.map;

        if (this.collection.markers.length === undefined || this.collection.markers.length === null){
            console.log('undefined length');
        } else if (this.collection.markers.length === 1){
            this.model = this.collection.markers[0].attributes;
            this.marker = L.marker([this.model.latitude, this.model.longitude]).addTo(this.map);
            this.bindEvent(this.marker, this.model);
        } else {
            this.addCollectionToMap(this.collection.markers.models);
        }
    },

    addCollectionToMap: function(arrayOfModels){
        var myIcon = L.Icon.extend({
            iconUrl: 'static/i/leaflet/blue-earthquake-pin-small.png',
            iconSize: [38, 95],
            iconAnchor: [22, 94],
            popupAnchor: [-3, -76]
        });

        this.markerCluster = L.markerClusterGroup({
            disableClusteringAtZoom: 8,
            zoomToBoundsOnClick: true,
            showCoverageOnHover: false
        });

        for(var i=0; i<arrayOfModels.length; i++){

            if (arrayOfModels[i].attributes.mag >= 4){
                this.marker = new L.CircleMarker([arrayOfModels[i].attributes.latitude, arrayOfModels[i].attributes.longitude], {
                    radius: 15,
                    color: '#9e4100',
                    fillColor: '#ec7c2d',
                    fillOpacity: 1.0,
                    opacity: 1.0,
                    weight: 5.0,
                    clickable: true
                });

            } else if (arrayOfModels[i].attributes.mag < 4 && arrayOfModels[i].attributes.mag > 2.5){
                this.marker = new L.CircleMarker([arrayOfModels[i].attributes.latitude, arrayOfModels[i].attributes.longitude], {
                    radius: 10,
                    color: '#9e4100',
                    fillColor: '#ec7c2d',
                    fillOpacity: .8,
                    opacity: .8,
                    weight: 1.0,
                    clickable: true
                });

            } else {
                this.marker = new L.CircleMarker([arrayOfModels[i].attributes.latitude, arrayOfModels[i].attributes.longitude], {
                    radius: 5,
                    color: '#9e4100',
                    fillColor: '#ec7c2d',
                    fillOpacity: .5,
                    opacity: .5,
                    weight: 1.0,
                    clickable: true
                });
            }

            this.bindEvent(this.marker, arrayOfModels[i].attributes);
            this.markerCluster.addLayer(this.marker);
        };

        this.map.addLayer(this.markerCluster);
    },

    bindEvent: function(marker, attributes){
        marker.on("click", function(){
            marker.bindPopup(
                "<div class='map-marker'>"+
                    "<article>" +
                        "<a href='" + attributes.earthquake_tracker_url + "'>" +
                            "<h1>" + moment(attributes.pacific_timezone).format('MMMM D, YYYY, h:mm a') + "</h1>" +
                            "<ul>" +
                                "<li class='near'><strong>Location</strong>: " + attributes.place + "</li>" +
                            "</ul>" +
                            "<aside class='magnitude'><strong>Magnitude</strong>: " + attributes.mag + "</aside>" +
                        "</a>" +
                    "</article>" +
                "</div");
        }).openPopup();

        /*
        marker.on('click', function(){
            var html = _.template(template("static/templates/details-full-view.html"), attributes);
            $(".data-display").html(html);
        });
        */
    }
});