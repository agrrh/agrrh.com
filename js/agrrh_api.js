var web_url = "//" + window.location.hostname + "/"

var api_url = "//agrrh.com/api/"
//var web_url = "//agrrh.com/"

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
        $("#tree_data").html("");

        $.get( api_url, function(data) {
            $.each(data['childs'], function(index, child) {
                $("#tree_data").append(
                    '<p><span class="fa fa-file-text-o"></span> <a href="' + web_url + child + '">' + child + '</a></p>'
                );
            });
        });
    });
}

function nav_data_feed() {
    $( document ).ready(function() {
        $.get( "https://api.github.com/repos/agrrh-/agrrh.com/commits", function( data ) {
            $("#github_data").html("");

            var i = 0;

            while (i < 5) {
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

nav_data_feed();
nav_github_feed();
