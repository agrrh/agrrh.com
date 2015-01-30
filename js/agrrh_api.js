var api_url = "//" + window.location.hostname + ":5000/"
//var api_url = "//127.0.0.1:5000/"

function nav_set_onclick(subject) {
    var link = "a_" + subject
    var query = subject + ".md"

    $("#" + link).click(
        function(e){
            $("#post_icon").attr("class", "fa fa-spin fa-spinner");
            $("#post_title").html('Loading');
            $("#post_data").html('...');

            $.get( api_url + query, function( data ) {
                $("#post_icon").attr("class", "fa fa-file-text-o");
                $("#post_title").html(data['title']);
                $("#post_data").html(data['data']);

                $(".active").removeClass("active");
                $("#" + link).parent().attr("class", "active");
            });

            return false;
        }
    );
}

function nav_github_feed() {
    $( document ).ready(function() {
        $.get( "https://api.github.com/repos/agrrh-/agrrh.com/commits", function( data ) {
            $("#github_data").html("");

            console.log(data);

            var i = 0;

            while (i < 5) {
                console.log(data[i]);
                item = data[i]

                $("#github_data").append(
                    '<p class="text-right">' +
                    item['commit']['message'] + ' ' +
                    '<a class="small" href="'+item['html_url']+'">@'+item['sha'].substring(0,7)+'</a>' +
                    '</p>'
                );

                i++;
            }
        });
    });
}

// -----------------------------------------------------

nav_set_onclick("about");
nav_set_onclick("contacts");

nav_github_feed();
