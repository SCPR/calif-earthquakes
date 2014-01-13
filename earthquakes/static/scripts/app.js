// create basic object to house application
(function(){
    window.App = {
        Models: {},
        Collections: {},
        Views: {},
        Router: {},
    };

    window.template = function(url){
        var data = "<h1> failed to load url : " + url + "</h1>";
        $.ajax({
            async: false,
            dataType: "text",
            url: SITE_URL + url,
            success: function(response) {
                data = response;
            }
        });
        return data;
    };

    $(function(){
        window.router = new App.Router();
        Backbone.history.start({
            root: '/',
            pushState: true,
        });
    });

    if ($(".column-chart").length) {
        $(".column-chart").each(function(){
            var myValue = $(this).attr("data-value");
            var myMax = $(this).attr("data-max");
            var proportionalHeight = (myValue / myMax) * 100;
            $(this).find(".fill").css("height",proportionalHeight + "%");
            if($(this).hasClass("from-floor")) {
                $(this).find(".label").css("top",(100 - proportionalHeight) + "%");
            } else if($(this).hasClass("from-ceiling")) {
                $(this).find(".label").css("top",proportionalHeight + "%");
            }
        });
    }

    if ($(".tip").length) {
        var whichDefinition;
        $(".tip").click(function(){
            window.scroll(0,0);
            whichDefinition = $(this).attr("href");
            $(whichDefinition).addClass("current");
            $("body").addClass("help-mode");
            return false;
        });
        $("button").click(function(){
            $(".definition.current").removeClass("current");
            $("body").removeClass("help-mode");
        });
    }

})();