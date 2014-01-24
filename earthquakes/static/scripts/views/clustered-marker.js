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
                "<p>" + moment(attributes.date_time).format('MMMM D, YYYY') + "<br />" +
                attributes.place + "<br />" +
                "Mag: " + attributes.mag + "</p>");
        }).openPopup();

        /*
        marker.on('click', function(){
            var html = _.template(template("static/templates/details-full-view.html"), attributes);
            $(".data-display").html(html);
        });
        */
    }
});