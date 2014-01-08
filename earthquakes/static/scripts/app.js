// create basic object to house application
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

    // shortcut function to render templates based on separate files
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

    // launch the router and start the history
    /*
    $(function(){
        window.router = new App.Router();
        Backbone.history.start({
            root: '/',
            pushState: false,
        });
    });
    */

})();