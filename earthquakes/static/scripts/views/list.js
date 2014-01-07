App.Views.ItemView = Backbone.View.extend({
    tagName: "div",
    className: "row",
    template: _.template(template("static/templates/list-view.html")),
    events: {
        "click a": "navigate"
    },
    navigate: function(e){
        e.preventDefault();

        // pass the model id to the router to the view
        var id = this.model.get("id");
        window.router.navigate("#earthquakes/" + id, {
            trigger: true,
            replace: false,
        });
    },
    render: function(){
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    }
});

App.Views.ListView = Backbone.View.extend({
    tagName: "div",
    className: "col-xs-12 col-sm-12 col-md-12 col-lg-12",
    initialize: function(){
        // bind the model to the anchor tag
        _.bindAll(this, "render");
    },
    render: function(){
        window.earthquakeCollection.each(function(earthquake){
            var itemView = new App.Views.ItemView({
                model: earthquake
            });
            this.$el.append(itemView.render().el);
        }, this);
        return this;
    }
});