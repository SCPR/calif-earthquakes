App.Views.MarkerView = Backbone.View.extend({

    initialize: function(markersInstance) {

        console.log('marker view initialized');

        console.log(markersInstance);

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

        //this.marker = L.marker([this.model.get('latitude'), this.model.get('longitude')], {icon: new myIcon({iconUrl: 'static/images/camera.png'})});

        //this.map = markersInstance.map;
        //this.marker = L.marker([this.model.get('latitude'), this.model.get('longitude')]).addTo(this.map);
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