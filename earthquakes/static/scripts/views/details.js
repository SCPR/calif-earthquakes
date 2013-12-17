App.Views.DetailView = Backbone.View.extend({

    el: '#earthquake-entries',

    template: _.template(template("static/templates/detail-view.html")),

    initialize: function(){
        this.render();
    },

    render: function () {
        console.log(this.model);
        this.$el.html(this.template(this.model[0].toJSON()));
        return this;
    }

});