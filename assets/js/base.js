jQuery(function($) {

    // Ensure "buttons" work 
    $(".button").live("click", function(evt) {
        var button = $(this);
        if(button.is(".submit") || button.is("button")) {
            button.closest("form").submit();
            button.attr("disabled", "disabled");
        }
        else if(button.is(".none")) {
            return false;
        }
        else {
            location.href = button.find("a").attr("href");
        }
    });
    
    // Post reply modal
    var reply = $('.reply').bind('click', function(evt) {
        evt.preventDefault();

        $(this).parents('.fancy').parent().find('.reply-modal').dialog({
            title: 'Comment reply',
            modal: true
        });

        return false;
    }).delegate('form', 'submit', function() {
      // what goes in hurr?
    });

    // Comment fancybox
    $('.thumbnail').fancybox();
    
    // Comment modals
    $('#add-video, #add-picture').bind('click', function(evt) {
        evt.preventDefault();
        evt.stopPropagation();
        
        var modalClass = $(this).attr('id'),
            pic = $("#picture"),
            yt = $("#yt-url"),
            hidden = $(".hidden"),
            _;

        $('.' + modalClass).dialog({
            modal: true,
            title: modalClass.replace('-', ' '),
            buttons: { 
                "add": function() { 
                    $("[name=yt-url]").val(yt.val());
                    _ = pic.clone(true);
                    pic.after(_);
                    hidden.empty().append(pic.attr("name", "picture"));
                    $(this).dialog("close");
                }
            }
        });

    });
    
    // Game Points earned modal
    $('.gamemodal').dialog({
        title: 'Hey Player!',
        modal: true,
        width: 300,
        height: 300
    });

    // Comment count
    var comments = $('#comment, #comments').find('textarea#id_message').bind('change keyup keydown blur', function(evt) {
        var len = 140 - this.value.length;
        if(len < 0 && evt.which !== 8 && evt.which !== 46) {
            return false;
        }
        comments.find('.count').text(len);
    }).end().attr('maxlength', '140');

    // Hide nested comments initially
    comments.find(".nested").children().hide();
    comments.delegate(".expand", "click", function() {
        $(this).removeClass("expand").addClass("collapse").html("<span>[-]</span> Collapse Replies").parent().children(".nested").show().children("li").show();
    });

    comments.delegate(".collapse", "click", function() {
        $(this).removeClass("collapse").addClass("expand").html("<span>[+]</span> Expand Replies").parent().children(".nested").hide().children("li").hide();
    });
    
    // Notifications code
    if (window.webkitNotifications) {
        if (window.webkitNotifications.checkPermission() == 0) { // 0 is PERMISSION_ALLOWED
            window
                .webkitNotifications
                .createNotification(
                    '/assets/img/logo.png',
                    'title',
                    'the notification body text goes here'
                ).show();
        } else {
            window.webkitNotifications.requestPermission();
        }
        
    } else  {
        
    }
});
