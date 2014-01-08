App.Views.ClusteredMarkerView = Backbone.View.extend({

    initialize: function(markersCollection) {

        // if else gymnastics to set marker icon based on params

        /*
        var myIcon = L.Icon.extend({
            iconUrl: 'images/camera.png',
            iconSize: [38, 95],
            iconAnchor: [22, 94],
            popupAnchor: [-3, -76]
        });

        if (this.model.attributes.result_type === 'instagram'){
            this.marker = L.marker([this.model.get('latitude'), this.model.get('longitude')], {icon: new myIcon({iconUrl: 'static/images/new-instagram-logo.png'})});
        } else {
            this.marker = L.marker([this.model.get('latitude'), this.model.get('longitude')], {icon: new myIcon({iconUrl: 'static/images/new-twitter-logo.png'})});
        }
        */

        /* some gymnastics here to determine if should rendere a clustered map
        or a single marker map. these should really be different views similar to
        the items? maybe i pass the logic in the router sted of here. */

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
        this.markerCluster = L.markerClusterGroup({
            disableClusteringAtZoom: 15
        });

        for(var i=0; i<arrayOfModels.length; i++){
            this.marker = L.marker(L.latLng(arrayOfModels[i].attributes.latitude, arrayOfModels[i].attributes.longitude));
            this.bindEvent(this.marker, arrayOfModels[i].attributes);
            this.marker.addTo(this.map);
            //this.markerCluster.addLayer(this.marker);
        };

        //this.map.addLayer(this.markerCluster);
    },

    bindEvent: function(marker, attributes){

        marker.on('click', function(){
            console.log(attributes);
        });

        //var that = this;
        //this.marker.on('click', function(){

            //console.log(that.model.attributes);

            // gymnastics to do something with marker data onclick
            /*
            $('#content-background').css({'opacity' : '0.7'}).fadeIn('fast');
            $('#content-display').html(that.template(that.model.attributes)).append('<button type="button"class="btn btn-danger btn-group btn-group-justified" id="close">Close</button>').fadeIn('slow');

            $('#close').click(function(){
                $('#content-display').fadeOut('fast');
                $('#content-background').fadeOut('fast');
            });

        	$('#content-background').click(function(){
        		$('#content-background').fadeOut('slow');
        		$('#content-display').fadeOut('slow');
        	});

        	$(document).keydown(function(e){
        		if(e.keyCode==27) {
        			$('#content-background').fadeOut('slow');
        			$('#content-display').fadeOut('slow');
        		}
        	});
            */

        //});

    }
});