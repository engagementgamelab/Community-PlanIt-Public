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
        $(this).parents('.controls').find('.reply-modal').slideUp(200);
        $(this).parents('.controls').find('.reply').show();
        return false;
    });

    // Post reply modal
    var reply = $('.reply').bind('click', function(evt) {
        evt.preventDefault();

        $(this).parents('.controls').find('.reply-modal').slideDown(200);
        $(this).hide();

        return false;
    }).delegate('form', 'submit', function() {
        $(this).slideUp(200);
    });

    // Comment fancybox
    $('.thumbnail').fancybox();
    
    // Comment modals
    $('#add-video, #add-picture').bind('click', function(evt) {
        evt.preventDefault();
        evt.stopPropagation();

        var form = $('#attachments .' + this.id);
        form.slideToggle(200);
        var inputs = form.find('textarea, input');
        if (inputs.val()) {
            form.find('.reset').text('remove');
        } else {
            form.find('.reset').text('cancel');
        }
    });

    $('#attachments .form .button').click(function(evt) {
        evt.preventDefault();
        evt.stopPropagation();

        var form = $(this).parents('.form');

        var inputs = form.find('textarea, input');
        if ($(this).hasClass('reset')) {
            inputs.val('');
        }
        
        var media = 'No media attached.';
        $('#attachments input, #attachments textarea').each(function(i) {
            if ($(this).val()) {
                media = 'Media attached.';
            }
        });
        $('#attachments .notification').html(media)

        form.slideUp(200);
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
