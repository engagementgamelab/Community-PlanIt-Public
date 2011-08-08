var CPI = CPI ? CPI: new Object();

CPI.mask = '<div class="mask"></div>';

CPI.sort_comments_by_activity = function(evt) {
    evt.preventDefault();
    evt.stopPropagation();

    $('#comments ul.comments').css('cursor', 'wait');
    $('#comments ul.comments').append($(CPI.mask));
    $('#comments ul.comments .mask').fadeIn(200);
    var comments = [];
    $('#comments ul.comments>li').each(function(i) {
        var comments_in_thread = $('li.comment', $(this)).size() + 1;
        var like_counts = $(this).find('.likes .count').map(function() {
            return Number($(this).text());
        });
        for (var i = 0, likes = 0; i < like_counts.size(); likes += like_counts[i++]);
        comments.push({'comment': $(this).detach(), 'activity': comments_in_thread + likes});
    });
    comments.sort(function(o1, o2) {
        var cmp =  o2.activity - o1.activity;
        if (cmp === 0) {
            cmp = o2.data('timestamp') - o1.data('timestamp');
        }
        return cmp;
    });
    for (var i = 0; i < comments.length; i++) {
        $('#comments ul.comments').append(comments[i].comment);
    }
    $('#comments ul.comments .mask').fadeOut(200, function() {
        $('#comments ul.comments .mask').remove();
        $('#comments ul.comments').css('cursor', 'auto');
    });
    return false;
}

CPI.sort_comments_by_timestamp = function(evt) {
    evt.preventDefault();
    evt.stopPropagation();

    $('#comments ul.comments').css('cursor', 'wait');
    $('#comments ul.comments').append($(CPI.mask));
    $('#comments ul.comments .mask').fadeIn(200);
    var comments = [];
    $('#comments ul.comments>li').each(function(i) {
        comments.push($(this).detach());
    });
    comments.sort(function(o1, o2) {
        return o2.data('timestamp') - o1.data('timestamp');
    });
    for (var i = 0; i < comments.length; i++) {
        $('#comments ul.comments').append(comments[i]);
    }
    $('#comments ul.comments .mask').fadeOut(200, function() {
        $('#comments ul.comments .mask').remove();
        $('#comments ul.comments').css('cursor', 'auto');
    });
    return false;
}

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

    $('.togglereplies').live('click', function(evt) {
        var replies = $($(this).attr('href'));
        replies.toggle();
        if (replies.is(':visible')) {
            $('.closed', this).hide();
            $('.open', this).show();
        } else {
            $('.open', this).hide();
            $('.closed', this).show();
        }
        return false;
    });
    
    $('.comment_sort_activity').click(CPI.sort_comments_by_activity);
    $('.comment_sort_time').click(CPI.sort_comments_by_timestamp);

    var reply = $('.cancel').bind('click', function(evt) {
        $(this).parents('.controls').find('.reply-modal').slideUp(200);
        $(this).parents('.controls').find('.actions').show();
        return false;
    });

    // Post reply modal
    var reply = $('.reply').bind('click', function(evt) {
        evt.preventDefault();

        $(this).parents('.controls').find('.reply-modal').slideDown(200);
        $(this).parents('.controls').find('.actions').hide();

        return false;
    }).delegate('form', 'submit', function() {
        $(this).slideUp(200);
    });

    // Comment fancybox
    $('.thumbnail').fancybox();
    
    // Comment modals
    $('a.add-video, a.add-picture').bind('click', function(evt) {
        evt.preventDefault();
        evt.stopPropagation();

        var form = $(this).parents('.attachments').find('.form.' + this.id);
        form.slideToggle(200);
        var inputs = form.find('textarea, input');
        if (inputs.val()) {
            form.find('.reset').text('remove');
        } else {
            form.find('.reset').text('cancel');
        }
    });

    $('.attachments .form .button').click(function(evt) {
        evt.preventDefault();
        evt.stopPropagation();

        var form = $(this).parents('.form');

        var inputs = form.find('textarea, input');
        if ($(this).hasClass('reset')) {
            inputs.val('');
        }
        
        var media = 'No media attached.';
        $('.attachments input, .attachments textarea').each(function(i) {
            if ($(this).val()) {
                media = 'Media attached.';
            }
        });
        $('.attachments .notification').html(media)

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
