App.Views.ItemView = Backbone.View.extend({
    tagName: "div",
    className: "row",
    template: _.template(template("static/templates/list-view.html")),
    events: {
        "click a": "navigate"
    },

    navigate: function(e){
        e.preventDefault();
        var primary_id = this.model.get("primary_id");
        this.earthquakeDetail = new App.Views.DetailView({
            model: this.model
        });

        window.router.navigate('#earthquakes/' + primary_id, {
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
    el: '#earthquake-entries',
    tagName: "div",
    className: "col-xs-12 col-sm-12 col-md-12 col-lg-12",
    initialize: function(){
        _.bindAll(this, "render");
    },
    render: function(){
        this.collection.each(function(earthquake){
            var itemView = new App.Views.ItemView({
                model: earthquake
            });
            this.$el.append(itemView.render().el);
        }, this);
        return this;
    }
});