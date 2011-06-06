jQuery(function($) {

    // Ensure "buttons" work 
    $(".button").live("click", function(evt) {
        var button = $(this);
        if(button.is(".submit") || button.is("button[type=submit]")) {
            button.closest("form").submit();
            button.attr("disabled", "disabled");
        }
        else if(button.is(".none") || button.is("button[type=reset]")) {
            return false;
        }
        else {
            location.href = button.find("a").attr("href");
        }
    });
    
    var reply = $('.cancel').bind('click', function(evt) {
        $(this).parents('.controls').find('.reply-modal').slideUp();
        $(this).parents('.controls').find('.reply').show();
        return false;
    });

    // Post reply modal
    var reply = $('.reply').bind('click', function(evt) {
        evt.preventDefault();

        $(this).parents('.controls').find('.reply-modal').slideDown();
        $(this).hide();

        return false;
    }).delegate('form', 'submit', function() {
        $(this).slideUp();
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
