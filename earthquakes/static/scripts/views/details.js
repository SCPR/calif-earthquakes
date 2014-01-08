App.Views.DetailView = Backbone.View.extend({
    template: _.template(template("static/templates/detail-view.html")),
    constructChartCss: function(){
        if (this.$(".column-chart").length) {
            this.$(".column-chart").each(function(){
                var myValue = $(this).attr("data-value");
                var myMax = $(this).attr("data-max");
                var proportionalHeight = (myValue / myMax) * 100;
                $(this).find(".fill").css("height", proportionalHeight + "%");
                if($(this).hasClass("from-floor")) {
                    $(this).find(".label").css("top",(100 - proportionalHeight) + "%");
                } else if ($(this).hasClass("from-ceiling")) {
                    $(this).find(".label").css("top",proportionalHeight + "%");
                }
            });
        }
    },
    render: function(){
        this.$el.html(this.template(this.model.toJSON()));
        this.constructChartCss();
        return this;
    }
});