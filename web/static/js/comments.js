/* Comments.js requires Masonry + Sijax */
/* 
    {# masonry is required to display comments correctly #}
    <script src="{{ STATIC_URL }}js/jquery.masonry.min.js"></script>
    <script src="{{ STATIC_URL }}js/sijax.js"></script>
    <script src="{{ STATIC_URL }}js/comments.js"></script>
*/
jQuery(function($) {
    
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


    $('.btn-like:not(.active)').live('click', function(e){
            $this = $(this);
            $.get($this.attr('data-url'), function(data) {
                    $this.addClass('active');
                    $('#id_likes-count-'+$this.attr('data-commentid')).html(data);
            });
    });

    $(".btn-reply").click(function(e){
            e.preventDefault();
            var form = $('#id_comment-form-'+$(this).attr('id'))[0];
            var form_data = Sijax.getFormValues('#id_comment-form-'+$(this).attr('id'));
            Sijax.request('create_comment', [form_data]);
            form.reset();
    });

    /* Masonry is a piece of javascript used to layout comments ('bricks') into columns floating left and upwards */

    /* Modify Masonry to support "Corner Stamp" for the heat-map legend */
    $.Mason.prototype.resize = function() {
            this._getColumns();
            this._reLayout();
    };
    $.Mason.prototype._reLayout = function( callback ) {
            var freeCols = this.cols;
            if ( this.options.cornerStampSelector ) {
            var $cornerStamp = this.element.find( this.options.cornerStampSelector ),
                    cornerStampX = $cornerStamp.offset().left - 
                        ( this.element.offset().left + this.offset.x + parseInt($cornerStamp.css('marginLeft')) );
            freeCols = Math.floor( cornerStampX / this.columnWidth );
            }
            // reset columns
            var i = this.cols;
                    this.colYs = [];
            while (i--) {
                    this.colYs.push( this.offset.y );
            }
            for ( i = freeCols; i < this.cols; i++ ) {
                    this.colYs[i] = this.offset.y + $cornerStamp.outerHeight(true);
            }
            // apply layout logic to all bricks
            this.layout( this.$bricks, callback );
    };
                
    init_masonry = function(callback){
            $('.comments').masonry({
                    // options
                    itemSelector : '.thread',
                    columnWidth : 320,
                    cornerStampSelector: '#corner-stamp'
            });
            if(typeof callback === 'function' && callback()){                
                callback();
            }
    }

    $('.thread-tail').hide();
    
    var hash = window.location.hash;
    $(hash).parents('.thread-tail').show();
    

    $('.btn-replies').click(function(){
        $(this).parents('.comment').next('.thread-tail').toggle(200, init_masonry);
        $(this).toggleClass('active');
    });

    /* Character Limit Counter */
    var type_count = function(evt) {
            var comment_form = $(this.form);
            var val = this.value.replace(/\r?\n/g, 'xx');
            var len = Math.max(0, 1000 - val.length);
            comment_form.find('.count').text(len);
            if (len < 1) {
                    comment_form.find('.reply-comment-counter').addClass('limited');
                    if (!(evt.ctrlKey || evt.which < 48 && evt.which !== 9 && evt.which !== 13)) {
                            return false;
                    }
            }
            comment_form.find('.reply-comment-counter').removeClass('limited');
    }
    $('#message_area, #id_response').live('change keyup keydown blur', type_count).attr('maxlength', '1000').change();
    $('#message_area, #id_response').limit('1000','#charsLeft');

    /* Toggle Attachments */
    $('.attachments-container').hide();
    $('.attachments-instructions').click(function(){
            $(this).toggleClass('active');
            $(this).next('.attachments-container').toggle();
    });
    
});


$(window).bind("load", function() {
    /* Make sure init_masonry runs last so that it calculates after css/images are loaded */
    init_masonry(function(){
        var hash = window.location.hash;
        window.location.hash = '';
        window.location.hash = hash;
    });
});