App.Views.Initialize = Backbone.View.extend({
    initialize: function(){
        // create instance of our collection
        this.earthquakeCollection = new App.Collections.Earthquakes();

        this.earthquakeCollection.reset();

        // fetch data to add to our collection
        this.earthquakeCollection.fetch({
            async: false,
        });

        // create instance of our items view
        this.earthquakeListView = new App.Views.Items({
            collection: this.earthquakeCollection
        });

        // render the items view
        $("#earthquake-entries").append(this.earthquakeListView.render().el);
    },
});