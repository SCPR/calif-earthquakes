App.Views.ClusteredMarkerView = Backbone.View.extend({

    initialize: function(markersCollection) {

        /* set the variable for the
        map the markers will be added to */
        this.map = markersCollection.map;

        /*
        var myIcon = L.Icon.extend({
            iconUrl: 'images/camera.png',
            iconSize: [38, 95],
            iconAnchor: [22, 94],
            popupAnchor: [-3, -76]
        });
        */

        // if else gymnastics to set marker icon based on params
        /*
        if (this.model.attributes.result_type === 'instagram'){
            this.marker = L.marker([this.model.get('latitude'), this.model.get('longitude')], {icon: new myIcon({iconUrl: 'static/images/new-instagram-logo.png'})});
        } else {
            this.marker = L.marker([this.model.get('latitude'), this.model.get('longitude')], {icon: new myIcon({iconUrl: 'static/images/new-twitter-logo.png'})});
        }
        */

        /* some gymnastics here to determine if should rendere a clustered map
        or a single marker map. these should really be different views similar to
        the items? maybe i pass the logic in the router sted of here. */

        if (markersCollection.markers.length === undefined || markersCollection.markers.length === null){
            console.log('undefined length');

        } else if (markersCollection.markers.length === 1){
            this.model = markersCollection.markers[0].attributes;
            this.marker = L.marker([this.model.latitude, this.model.longitude]).addTo(this.map);
            //this.marker.bindPopup('single boom');
            this.bindEvent(this.marker, this.model);

        } else {
            this.markerCluster = L.markerClusterGroup({
                disableClusteringAtZoom: 15
            });
            this.markerInstance = markersCollection.markers.models;
            for(var i=0; i<this.markerInstance.length; i++){
                this.marker = L.marker(L.latLng(this.markerInstance[i].attributes.latitude, this.markerInstance[i].attributes.longitude));
                //this.marker.bindPopup('cluster boom');
                this.bindEvent(this.marker, this.markerInstance[i].attributes);
                this.markerCluster.addLayer(this.marker);
            };

            var laCounty = L.geoJson(losAngelesCounty, {
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
                        console.log(feature.properties.name + ' county layer clicked');
                    });
                }
            });

            var laCountyFaults = L.geoJson(losAngelesCountyFaults, {
                style: function (feature) {
                    return {
                        color: 'green',
                        weight: 2,
                        opacity: 1,
                        fillColor: null,
                        fillOpacity: 0
                    }
                },
                onEachFeature: function(feature, layer) {
                    layer.on('click', function (e) {
                        console.log(feature.properties.NAME + ' fault line clicked');
                    });
                }
            });
            this.markerCluster.addLayer(laCountyFaults);
            this.markerCluster.addLayer(laCounty);
            this.map.addLayer(this.markerCluster);
            //this.map.fitBounds(this.markerCluster.getBounds());
        }

    },

    bindEvent: function(marker, attributes){

        marker.on('click', function(){
            console.log(attributes);
        });

    }

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



});