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

        $(this).parents('.fancy').find('.reply-modal').dialog({
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
                    $('#attachments .notification').html('Media attached!')
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
    $('textarea.comment_message').live('change keyup keydown blur', function(evt) {
        var comment_form = $(this.form);
        var val = this.value.replace(/\r?\n/g, 'xx');
        var len = Math.max(0, 1000 - val.length);
        comment_form.find('.count').text(len);
        if (len < 1) {
            comment_form.find('.counter').addClass('limited');
            if (!(evt.ctrlKey || evt.which < 48 && evt.which !== 9 && evt.which !== 13)) {
                return false;
            }
        }
        comment_form.find('.counter').removeClass('limited');
    }).attr('maxlength', '1000').change();

    var comments = $('#comments');
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
