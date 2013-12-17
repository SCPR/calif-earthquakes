App.Views.Item = Backbone.View.extend({
    tagName: "div",

    className: "row",

    template: _.template(template("static/templates/list-view.html")),

    //template: $('#listView').html(),

    events: {
        'click a': 'navigate'
    },

    navigate: function(e){
        e.preventDefault();
        var modelId = this.model.attributes.primary_id;
        window.app.navigate('#earthquakes/' + modelId, {
            trigger: true,
            replace: false,
        });
    },

    render: function () {
        this.$el.html(this.template(this.model.toJSON()));
        return this;

        /*
        var source = this.template;
        var template = Handlebars.compile(source);
        var html = template(this.model.toJSON());
        $(this.el).html(html);
        return this;
        */
    }
});

App.Views.Items = Backbone.View.extend({
    tagName: "div",
    className: "col-xs-12 col-sm-12 col-md-12 col-lg-12",
    render: function(){
        this.collection.each(function(earthquake){
            var itemView = new App.Views.Item({
                model: earthquake
            });
            this.$el.append(itemView.render().el);
        }, this);
        return this;
    }
});