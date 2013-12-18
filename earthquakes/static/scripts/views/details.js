App.Views.DetailView = Backbone.View.extend({
    el: '#earthquake-entry',
    template: _.template(template("static/templates/detail-view.html")),
    initialize: function(){
        this.render();
    },
    render: function () {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    }
});