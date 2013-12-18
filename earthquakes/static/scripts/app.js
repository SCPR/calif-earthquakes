(function(){

    window.App = {
        Models: {},
        Collections: {},
        Views: {},
        Router: {},
    };

    /*
    old shortcut function to render templates
    window.template = function(id){
        return _.template( $('#' + id).html());
    };
    */

    // new shortcut function to render templates based on separate files
    window.template = function(url){
        var data = "<h1> failed to load url : " + url + "</h1>";
        $.ajax({
            async: false,
            dataType: "text",
            url: url,
            success: function(response) {
                data = response;
            }
        });
        return data;
    };

    $(function(){
        window.router = new App.Router();
        //window.initialize = new App.Views.Initialize();
        Backbone.history.start({
            root: '/',
            pushState: false,
        });

    });

})();