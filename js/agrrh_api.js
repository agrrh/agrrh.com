var api_url = "//" + window.location.hostname + ":5000/"
//var api_url = "//127.0.0.1:5000/"

function nav_set_onclick(subject) {
    var link = "a_" + subject
    var query = subject + ".md"

    $("#" + link).click(
        function(e){
            $("#post_title").html('Loading');
            $("#post_data").html('<span class="fa fa-spin fa-spinner"></span>');

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
