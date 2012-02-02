var CPI = CPI ? CPI: new Object();

CPI.mask = '<div class="mask"></div>';

CPI.sort_comments_by_activity = function(evt) {
    evt.preventDefault();
    evt.stopPropagation();

    var comment_list = $('ul.comment_list');
    comment_list.css('cursor', 'wait');
    comment_list.append($(CPI.mask));
    $('.mask', comment_list).fadeIn(200);
    var comments = [];
    comment_list.children('li').each(function(i) {
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
            cmp = o2['comment'].data('timestamp') - o1['comment'].data('timestamp');
        }
        return cmp;
    });
    for (var i = 0; i < comments.length; i++) {
        comment_list.append(comments[i].comment);
    }
    $('.mask', comment_list).fadeOut(200, function() {
        $('.mask', comment_list).remove();
        comment_list.css('cursor', 'auto');
    });
    return false;
}

CPI.sort_comments_by_timestamp = function(evt) {
    evt.preventDefault();
    evt.stopPropagation();

    var comment_list = $('ul.comment_list');
    comment_list.css('cursor', 'wait');
    comment_list.append($(CPI.mask));
    $('.mask', comment_list).fadeIn(200);
    var comments = [];
    comment_list.children('li').each(function(i) {
        comments.push($(this).detach());
    });
    comments.sort(function(o1, o2) {
        return o2.data('timestamp') - o1.data('timestamp');
    });
    for (var i = 0; i < comments.length; i++) {
        comment_list.append(comments[i]);
    }
    $('.mask', comment_list).fadeOut(200, function() {
        $('.mask', comment_list).remove();
        comment_list.css('cursor', 'auto');
    });
    return false;
}

jQuery(function($) {

    // Ensure "buttons" work 
    $("a.button").live("click", function(evt) {
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


    // comments like button ajax
    $('div[id^=id_like-]').live("click", function(e){
        var comment_id = $(this).attr('id').replace('id_like-','');
        $.ajax({
            type: "GET",
            url: '/comments/ajax/like/'+ comment_id +'/',
            success: function(data, textStatus) {
                $('div[id=id_likes-count-'+comment_id+']').text(data);
            },
            error: function(data){}
        });
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

    if (window.location.hash.search(/^#comment-/) != -1) {
        $(window.location.hash).parents('.replies').show();
        $(window.location.hash).parents('.comment').find('.closed').hide();
        $(window.location.hash).parents('.comment').find('.open').show();
        $('.replies', window.location.hash).hide();
        $('.open', window.location.hash).hide();
        $('.closed', window.location.hash).show();
    }

    // Game Points earned modal
    $('.gamemodal').dialog({
        title: 'Hey Player!',
        modal: true,
        width: 300,
        height: 300
    });
    
    var type_count = function(evt) {
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
    }

     $.fn.extend({  
         limit: function(limit,element) {
			var interval, f;
			var self = $(this);
					
			$(this).focus(function(){
				interval = window.setInterval(substring,100);
			});
			$(this).blur(function(){
				clearInterval(interval);
				substring();
			});
			substringFunction = "function substring(){ var val = $(self).val(); if (val) {var length = val.length;if(length > limit){$(self).val($(self).val().substring(0,limit));}}";
			if(typeof element != 'undefined')
				substringFunction += "if($(element).html() != limit-length){$(element).html((limit-length<=0)?'0':limit-length);}"
			substringFunction += "}";
			eval(substringFunction);
			substring();
        } 
    }); 
    // Challenge description count
    $('textarea#id_description').live('change keyup keydown blur', type_count).attr('maxlength', '1000').change();
    
    // Comment count
    $('textarea#id_message').live('change keyup keydown blur', type_count).attr('maxlength', '1000').change();

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
