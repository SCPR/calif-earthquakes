App.Views.Initialize = Backbone.View.extend({
    initialize: function(){

        // create instance of our collection
        this.earthquakeCollection = new App.Collections.Earthquakes();

        // fetch data to add to our collection
        this.earthquakeCollection.fetch({
            async: false,
        });

        // create instance of our items view
        this.earthquakeList = new App.Views.ListView({
            collection: this.earthquakeCollection
        });

        // render the items view
        this.earthquakeList.render().el;
    },
});