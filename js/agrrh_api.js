//var api_url = "//" + window.location.hostname + ":5000/"
var api_url = "//10.0.51.11:5000/"

function nav_set_onclick(subject) {
    var link = "a_" + subject
    var query = subject + ".md"

    $("#" + link).click(
        function(e){
            $.get( api_url + query, function( data ) {
                $("#post_title").html(data['title']);
                $("#post_data").html(data['data']);

                $(".active").removeClass("active");
                $("#" + link).parent().attr("class", "active");
            });

            return false;
        }
    );
}

nav_set_onclick("about");
nav_set_onclick("contacts");
