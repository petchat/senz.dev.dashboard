//
//function escape_regexp(str) {
//  return str.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
//}
//
//function replace_all(find, replace, str) {
//  return str.replace(new RegExp(escape_regexp(find), 'g'), replace);
//}
//
//function init_log() {
//    var $log = $("#log");
//    function scroll_down($el) {
//        $el.scrollTop($el[0].scrollHeight);
//    }
//
//    function read_log() {
//        var $el = $("#log-content");
//        var mode = $el.data("mode");
//        if(mode != "tail") {
//            return;
//        }
//
//        $.get($log.data("read-log-url"), function (resp) {
//            // only scroll down if the scroll is already at the bottom.
//            if(($el.scrollTop() + $el.innerHeight()) >= $el[0].scrollHeight) {
//                $el.append(resp);
//                scroll_down($el);
//            } else {
//                $el.append(resp);
//            }
//        });
//    }
//
//    function exit_search_mode() {
//        var $el = $("#log-content");
//        $el.data("mode", "tail");
//        var $controls = $("#log").find(".controls");
//        $controls.find(".mode-text").text("Tail mode (Press s to search)");
//        $controls.find(".status-text").hide();
//
//        $.get($log.data("read-log-tail-url"), function (resp) {
//            $el.text(resp);
//            scroll_down($el);
//            $("#search-input").val("").blur();
//        });
//    }
//
//    $("#scroll-down-btn").click(function() {
//        scroll_down($el);
//    });
//
//    $("#search-form").submit(function(e) {
//        e.preventDefault();
//
//        var val = $("#search-input").val();
//        if(!val) return;
//
//        var $el = $("#log-content");
//        var filename = $el.data("filename");
//        var params = {
//            "filename": filename,
//            "text": val
//        };
//
//        $el.data("mode", "search");
//        $("#log").find(".controls .mode-text").text("Search mode (Press enter for next, escape to exit)");
//
//        $.get($log.data("search-log-url"), params, function (resp) {
//            var $log = $("#log");
//            $log.find(".controls .status-text").hide();
//            $el.find(".found-text").removeClass("found-text");
//
//            var $status = $log.find(".controls .status-text");
//
//            if(resp.position == -1) {
//                $status.text("EOF Reached.");
//            } else {
//                // split up the content on found pos.
//                var content_before = resp.content.slice(0, resp.buffer_pos);
//                var content_after = resp.content.slice(resp.buffer_pos + params["text"].length);
//
//                // escape html in log content
//                resp.content = $('<div/>').text(resp.content).html();
//
//                // highlight matches
//                var matched_text = '<span class="matching-text">' + params['text'] + '</span>';
//                var found_text = '<span class="found-text">' + params["text"] + '</span>';
//                content_before = replace_all(params["text"], matched_text, content_before);
//                content_after = replace_all(params["text"], matched_text, content_after);
//                resp.content = content_before + found_text + content_after;
//                $el.html(resp.content);
//
//                $status.text("Position " + resp.position + " of " + resp.filesize + ".");
//            }
//
//            $status.show();
//        });
//    });
//
//    $(document).keyup(function(e) {
//        var mode = $el.data("mode");
//        if(mode != "search" && e.which == 83) {
//            $("#search-input").focus();
//        }
//        // Exit search mode if escape is pressed.
//        else if(mode == "search" && e.which == 27) {
//            exit_search_mode();
//        }
//    });
//
//    setInterval(read_log, 1000);
//    var $el = $("#log-content");
//    scroll_down($el);
//}
//
//var skip_updates = false;
//
////function init_updater() {
////    function update() {
////        if (skip_updates) return;
////
////        $.ajax({
////            url: location.href,
////            cache: false,
////            dataType: "html",
////            success: function(resp){
////                $("#psdash").find(".main-content").html(resp);
////            }
////        });
////    }
////
////    setInterval(update, 3000);
////}
//
//function init_connections_filter() {
//    var $content = $("#psdash");
//    $content.on("change", "#connections-form select", function () {
//        $content.find("#connections-form").submit();
//    });
//    $content.on("focus", "#connections-form select, #connections-form input", function () {
//        skip_updates = true;
//    });
//    $content.on("blur", "#connections-form select, #connections-form input", function () {
//        skip_updates = false;
//    });
//    $content.on("keypress", "#connections-form input[type='text']", function (e) {
//        if (e.which == 13) {
//            $content.find("#connections-form").submit();
//        }
//    });
//}
//

function init_dom(){
    active_id = window.location.hash.substring(1);
    //console.log(active_id)
    if (active_id == 'signup'){
        $("#login-form").fadeOut(0);
        $("#register-form").fadeIn(0);

		$('#login-form-link').removeClass('active');
		$('#register-form-link').addClass('axctive');
        //e.preventDefault();
    }
    if (active_id == 'forgotpass'){
        $("#panel-login").fadeOut(0);
        $("#panel-forgotpass").fadeIn(0);

		//$('#login-form-link').removeClass('active');
		//$('#register-form-link').addClass('active');
        //e.preventDefault();
    }
}
$(document).ready(function() {
    init_dom();
});
$(function() {


    $('#login-form-link').click(function(e) {
		$("#login-form").delay(100).fadeIn(100);
 		$("#register-form").fadeOut(100);
		$('#register-form-link').removeClass('active');
		$(this).addClass('active');
		//e.preventDefault();
	});
	$('#register-form-link').click(function(e) {
		$("#register-form").delay(100).fadeIn(100);
 		$("#login-form").fadeOut(100);
		$('#login-form-link').removeClass('active');
		$(this).addClass('active');
		//e.preventDefault();
	});
    $('#forgot-password-link').click(function(e) {
        console.log('forgot-password-linking')
		$("#panel-login").fadeOut(0);
        $("#panel-forgotpass").fadeIn(0);
	});
    $('#newapp-link').click(function(e) {
		$("#newapp-view").delay(100).fadeIn(100);
 		$(".console-page").fadeOut(100);
		//$('#register-form-link').removeClass('active');
		//$(this).addClass('active');
		//e.preventDefault();
	});
    $('.btn-tracker').click(function(e){
        var tracker_id = $(this).attr("tracker_id");
        var app_id = $(".switch-app .dropdown button").attr("app_id")

         $(this).removeClass("btn-success");
        console.log($(this).text())
        console.log($(this).attr("class"))
         $(this).text("Tracked it!")
        console.log(tracker_id);
         $.post("/track",
             {
            tracker_id: tracker_id,
                 app_id: app_id

            },
             function(data,status){

             $(this).addClass("btn-default")

                 console.log(data+" "+status)
        });
    });
    $('.left-nav ul li a').click(function(e){
        e.preventDefault();
        var _xsrf = $("[name='_xsrf']").attr('value');
        var app_id = $(".switch-app .dropdown button").attr("app_id");
        console.log(_xsrf)
        console.log(app_id)

        $('.left-nav ul li[class="active"]').removeClass("active");
        $(this).parent().addClass("active");
        var href = $(this).attr('href');
        console.log(href);
        e.preventDefault();

        $.post(href,
             {
             _xsrf: _xsrf,
             app_id: app_id
            },
             function(data,status){
             $("#psdash").find(".main-content").html(data);
             $(this).addClass("btn-default")
        });
    })



    $(".alert").fadeTo(5000, 0.3).slideUp(2000, function(){
    $(".alert").alert('close');
});
});
