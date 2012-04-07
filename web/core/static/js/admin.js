jQuery(function( $ ) {
    // DoM cAcHe
    var links = $( '.addlink,.changelink' )
      , instances_select = $( '.instances_select' )
      , instances = $( '.instances' );

    var ajaxModel = function( sidebar ) {
      var self = {
        models: {}
      , table: 'table.html'
      , template: 'manage-pane.html'
      , _active: null
      , sidebar: sidebar
      };

      self.normalizeMeta = function( href ) {
        var meta = {};

        if(self._active && self._active._meta) {
          meta = self._active._meta;
        }
        else {
          meta = {
            current_href: href
          , add_href: href.split( '/' ).slice( 0, 2 ).join( '/' ) + '/add/' 
          , list_href: href.split( '/' ).slice( 0, 2 ).join( '/' ) + '/'
          , label: 'Manage'
          };
        }

        return meta;
      };

      // FIXME: Need to add back the edit links
      console.log('test');
      // Add edit link beside add another
      $( '.add-another' ).after(function() {
        console.log( arguments );
      });//'<a href="/admin/prompts/basicprompt/" class="changelink"></a>' );

      self.fetchTemplate = function() {
        var templates = {};
        // Close off the templates variable
        return function( name ) {
          // Create and return a deferred object
          return $.Deferred(function( def ) {
            // If in cache, return early
            if( name in templates ) {
              return def.resolve( templates[name] );
            }
            // Else ajax out
            $.get( MEDIA_URL + 'templates/' + name, function( data ) {
              templates[name] = data;
              return def.resolve( data );
            });
          }).promise();
        };
      }();

      self.render = function( html ) {
        // hack to get recent admin to show
        $.get( '/admin', function( data ) {
          $( 'body' ).find( '.module.activity' ).html( $(data).find( '.module.activity' ).html() );
        });

        sidebar.html( html );

        self.reload();
      };

      $( '.manage-pane' ).delegate( '.changelink', 'click', function() {
        var This = $( this ),
            id = parseInt( This.prevAll( 'select' ).val() );

        if( id > -1 ) {
          This.attr( 'href', '/admin/prompts/basicprompt/' + id + '/' );
          return showRelatedObjectLookupPopup( this );
        }
        else {
          window.alert('you need to add a foreign key before you can change it');
        }

        return false;
      });

      self.reload = function() {
        if( self._active && self._active._meta.label === 'Manage missions' ) {
          $( '.add-another' ).after( '<a href="/admin/prompts/basicprompt/" class="changelink"></a>' );
        }
        $( '.add-map' ).hide();
        window.setTimeout(function() {
          $.getScript( '/admin/gmapsfield/admin/admin.js' );
          $.getScript( '/admin-media/js/inlines.min.js' );

          DateTimeShortcuts.init();


          var rows = "#reference_set-group .tabular.inline-related tbody tr";
          var alternatingRows = function(row) {
              $(rows).not(".add-row").removeClass("row1 row2")
                  .filter(":even").addClass("row1").end()
                  .filter(rows + ":odd").addClass("row2");
          }
          var reinitDateTimeShortCuts = function() {
              // Reinitialize the calendar and clock widgets by force
              if (typeof DateTimeShortcuts != "undefined") {
                  $(".datetimeshortcuts").remove();
                  DateTimeShortcuts.init();
              }
          }
          var updateSelectFilter = function() {
              // If any SelectFilter widgets are a part of the new form,
              // instantiate a new SelectFilter instance for it.
              if (typeof SelectFilter != "undefined"){
                  $(".selectfilter").each(function(index, value){
                    var namearr = value.name.split('-');
                    SelectFilter.init(value.id, namearr[namearr.length-1], false, "/admin-media/");
                  })
                  $(".selectfilterstacked").each(function(index, value){
                    var namearr = value.name.split('-');
                    SelectFilter.init(value.id, namearr[namearr.length-1], true, "/admin-media/");
                  })
              }
          }
          var initPrepopulatedFields = function(row) {
              row.find('.prepopulated_field').each(function() {
                  var field = $(this);
                  var input = field.find('input, select, textarea');
                  var dependency_list = input.data('dependency_list') || [];
                  var dependencies = row.find(dependency_list.join(',')).find('input, select, textarea');
                  if (dependencies.length) {
                      input.prepopulate(dependencies, input.attr('maxlength'));
                  }
              });
          }
          $(rows).formset({
              prefix: "reference_set",
              addText: "Add another Reference",
              formCssClass: "dynamic-reference_set",
              deleteCssClass: "inline-deletelink",
              deleteText: "Remove",
              emptyCssClass: "empty-form",
              removed: alternatingRows,
              added: (function(row) {
                  initPrepopulatedFields(row);
                  reinitDateTimeShortCuts();
                  updateSelectFilter();
                  alternatingRows(row);
              })
          });

        var rows = "#games-mapit-content_type-object_id-group .inline-related";
        var updateInlineLabel = function(row) {
            $(rows).find(".inline_label").each(function(i) {
                var count = i + 1;
                $(this).html($(this).html().replace(/(#\d+)/g, "#" + count));
            });
        }
        var reinitDateTimeShortCuts = function() {
            // Reinitialize the calendar and clock widgets by force, yuck.
            if (typeof DateTimeShortcuts != "undefined") {
                $(".datetimeshortcuts").remove();
                DateTimeShortcuts.init();
            }
        }
        var updateSelectFilter = function() {
            // If any SelectFilter widgets were added, instantiate a new instance.
            if (typeof SelectFilter != "undefined"){
                $(".selectfilter").each(function(index, value){
                  var namearr = value.name.split('-');
                  SelectFilter.init(value.id, namearr[namearr.length-1], false, "/admin-media/");
                })
                $(".selectfilterstacked").each(function(index, value){
                  var namearr = value.name.split('-');
                  SelectFilter.init(value.id, namearr[namearr.length-1], true, "/admin-media/");
                })
            }
        }
        var initPrepopulatedFields = function(row) {
            row.find('.prepopulated_field').each(function() {
                var field = $(this);
                var input = field.find('input, select, textarea');
                var dependency_list = input.data('dependency_list') || [];
                var dependencies = row.find(dependency_list.join(',')).find('input, select, textarea');
                if (dependencies.length) {
                    input.prepopulate(dependencies, input.attr('maxlength'));
                }
            });
        }
        $(rows).formset({
            prefix: "games-mapit-content_type-object_id",
            addText: "Add another Mapit Game",
            formCssClass: "dynamic-games-mapit-content_type-object_id",
            deleteCssClass: "inline-deletelink",
            deleteText: "Remove",
            emptyCssClass: "empty-form",
            removed: updateInlineLabel,
            added: (function(row) {
                initPrepopulatedFields(row);
                reinitDateTimeShortCuts();
                updateSelectFilter();
                updateInlineLabel(row);
            })
        });
  var rows = "#games-thinkfast-content_type-object_id-group .inline-related";
        var updateInlineLabel = function(row) {
            $(rows).find(".inline_label").each(function(i) {
                var count = i + 1;
                $(this).html($(this).html().replace(/(#\d+)/g, "#" + count));
            });
        }
        var reinitDateTimeShortCuts = function() {
            // Reinitialize the calendar and clock widgets by force, yuck.
            if (typeof DateTimeShortcuts != "undefined") {
                $(".datetimeshortcuts").remove();
                DateTimeShortcuts.init();
            }
        }
        var updateSelectFilter = function() {
            // If any SelectFilter widgets were added, instantiate a new instance.
            if (typeof SelectFilter != "undefined"){
                $(".selectfilter").each(function(index, value){
                  var namearr = value.name.split('-');
                  SelectFilter.init(value.id, namearr[namearr.length-1], false, "/admin-media/");
                })
                $(".selectfilterstacked").each(function(index, value){
                  var namearr = value.name.split('-');
                  SelectFilter.init(value.id, namearr[namearr.length-1], true, "/admin-media/");
                })
            }
        }
        var initPrepopulatedFields = function(row) {
            row.find('.prepopulated_field').each(function() {
                var field = $(this);
                var input = field.find('input, select, textarea');
                var dependency_list = input.data('dependency_list') || [];
                var dependencies = row.find(dependency_list.join(',')).find('input, select, textarea');
                if (dependencies.length) {
                    input.prepopulate(dependencies, input.attr('maxlength'));
                }
            });
        }
        $(rows).formset({
            prefix: "games-thinkfast-content_type-object_id",
            addText: "Add another Think Fast! Game",
            formCssClass: "dynamic-games-thinkfast-content_type-object_id",
            deleteCssClass: "inline-deletelink",
            deleteText: "Remove",
            emptyCssClass: "empty-form",
            removed: updateInlineLabel,
            added: (function(row) {
                initPrepopulatedFields(row);
                reinitDateTimeShortCuts();
                updateSelectFilter();
                updateInlineLabel(row);
            })
        });
       var rows = "#games-othershoes-content_type-object_id-group .inline-related";
        var updateInlineLabel = function(row) {
            $(rows).find(".inline_label").each(function(i) {
                var count = i + 1;
                $(this).html($(this).html().replace(/(#\d+)/g, "#" + count));
            });
        }
        var reinitDateTimeShortCuts = function() {
            // Reinitialize the calendar and clock widgets by force, yuck.
            if (typeof DateTimeShortcuts != "undefined") {
                $(".datetimeshortcuts").remove();
                DateTimeShortcuts.init();
            }
        }
        var updateSelectFilter = function() {
            // If any SelectFilter widgets were added, instantiate a new instance.
            if (typeof SelectFilter != "undefined"){
                $(".selectfilter").each(function(index, value){
                  var namearr = value.name.split('-');
                  SelectFilter.init(value.id, namearr[namearr.length-1], false, "/admin-media/");
                })
                $(".selectfilterstacked").each(function(index, value){
                  var namearr = value.name.split('-');
                  SelectFilter.init(value.id, namearr[namearr.length-1], true, "/admin-media/");
                })
            }
        }
        var initPrepopulatedFields = function(row) {
            row.find('.prepopulated_field').each(function() {
                var field = $(this);
                var input = field.find('input, select, textarea');
                var dependency_list = input.data('dependency_list') || [];
                var dependencies = row.find(dependency_list.join(',')).find('input, select, textarea');
                if (dependencies.length) {
                    input.prepopulate(dependencies, input.attr('maxlength'));
                }
            });
        }
        $(rows).formset({
            prefix: "games-othershoes-content_type-object_id",
            addText: "Add another Other Shoes Game",
            formCssClass: "dynamic-games-othershoes-content_type-object_id",
            deleteCssClass: "inline-deletelink",
            deleteText: "Remove",
            emptyCssClass: "empty-form",
            removed: updateInlineLabel,
            added: (function(row) {
                initPrepopulatedFields(row);
                reinitDateTimeShortCuts();
                updateSelectFilter();
                updateInlineLabel(row);
            })
        });

        $('select[name^=games-]').find('option').remove('option:not([selected])');

        }, 100);
      };

      self.submit = function( evt ) {
        evt.preventDefault();

        var form = $( this )
          , href = form.attr( 'action' )
          , meta = self.normalizeMeta( href );

        // JS methods are case sensitive hence the toLowerCase
        var req = $[this.method.toLowerCase() || 'post']( meta.current_href, form.serialize() );

        // Initial
        $.when( self.fetchTemplate( self.template ), $.get( meta.add_href ), $.get( meta.list_href ), req ).then(
          function( template, edit, list ) {
            var view = {
              template: template[0]
            , edit: $( edit[0] ).find( '#content-main' ).html()
            , list: $( list[0] ).find( '#content-main' ).html()
            };

            // Error detected
            if( ~view.edit.indexOf( '<ul class="errorlist">' ) ) {
              self.render( Mustache.to_html( template, view, { error: true } ) );
            }
            // No error, success!
            else {
              self.render( Mustache.to_html( template, view, { error: false } ) );
            }
          }
        );

        return false;
      };

      self.update = function( evt ) {
        evt.preventDefault();

        var href = $( this ).attr( 'href' )
          , meta = self.normalizeMeta( href );

        meta.current_href = meta.base_href + href;
        var req = $.get( meta.current_href );

        $.when( self.fetchTemplate( self.template ), req, $.get( meta.list_href ) ).then(
          function( template, edit, list ) {
            var view = {
              template: template[0]
            , label: meta.label
            , edit: $( edit[0] ).find( '#content-main' ).html()
            , list: $( list[0] ).find( '#content-main' ).html()
            };

            self.render( Mustache.to_html( template, view ) );

            sidebar.find( 'form' ).attr( 'action', meta.current_href )
              .find( '.deletelink' ).attr( 'href', meta.base_href + href + 'delete/' );
          }
        );

        return false;
      };
      self.paging = function( evt ) {
        evt.preventDefault();

        var href = $( this ).attr( 'href' )
          , meta = self.normalizeMeta( href );

        meta.current_href = meta.base_href + href;

        $.when( self.fetchTemplate( self.template ), $.get( meta.add_href ), $.get( meta.current_href ) ).then(
          function( template, edit, list ) {
            var view = {
              template: template[0]
            , label: meta.label
            , edit: $( edit[0] ).find( '#content-main' ).html()
            , list: $( list[0] ).find( '#content-main' ).html()
            };

            self.render( Mustache.to_html( template, view ) );

            sidebar.find( 'form' ).attr( 'action', meta.current_href )
              .find( '.deletelink' ).attr( 'href', href + 'delete/' );
          }
        );

        return false;
      };

      self.remove = function( evt ) {
        evt.preventDefault();

        var href = $( this ).attr( 'href' )
          , meta = self.normalizeMeta( href );

        var req = $.post( href, { post: 'true' } );

        $.when( self.fetchTemplate( self.template ), $.get( meta.add_href ), $.get( meta.list_href ), req ).then(
          function( template, edit, list ) {
            var view = {
              template: template[0]
            , label: meta.label
            , edit: $( edit[0] ).find( '#content-main' ).html()
            , list: $( list[0] ).find( '#content-main' ).html()
            };

            self.render( Mustache.to_html( template, view ) );
          }
        );

        return false;
      };

      self.display = function( evt ) {
        evt.preventDefault();

        self._active = undefined;

        var href = $( this ).attr( 'href' )
          , label = ""
          , req = $.get( href )
          , meta = self.normalizeMeta( href );

        req.error(function() {
          sidebar.text( 'Object was deleted.' ).show();
        });

        $.when( self.fetchTemplate( self.template ), req, $.get( href.split('/').slice(0,2).join('/') ) ).then(
          function( template, edit, list ) {
            var view = {
              template: template[0]
            , label: 'Edit object'
            , edit: $( edit[0] ).find( '#content-main' ).html()
            , list: $( list[0] ).find( '#content-main' ).html()
            };

            self.render( Mustache.to_html( template, view ) );

            sidebar.find( 'form' ).attr( 'action', href )
              .find( '.deletelink' ).attr( 'href', meta.base_href + href.split('/').slice(2).shift() + '/delete/' );

            sidebar.show();
          }
        );

        return false;
      };

      self.instance = function( evt ) {
        evt.preventDefault();

        self._active = undefined;

        var href = $( this ).attr( 'href' )
          , label = ""
          , req = $.get( href )
          , meta = self.normalizeMeta( href );

        $.when( self.fetchTemplate( self.template ), req ).then(
          function( template, edit ) {
            var view = {
              template: template[0]
            , label: 'Edit object'
            , edit: $( edit[0] ).find( '#content-main' ).html()
            };

            self.render( Mustache.to_html( template, view ) );

            sidebar.find( 'form' ).attr( 'action', href + '/' )
              .find( '.deletelink' ).attr( 'href', meta.base_href + href.split('/').slice(2).shift() + '/delete/' );

            sidebar.show();
          }
        );

        return false;
      };

      sidebar.delegate( 'form', 'submit', self.submit );
      sidebar.delegate( '.deletelink', 'click', self.remove );
      sidebar.delegate( 'a:not([href^=javascript], [onclick])', 'click', self.update );
      sidebar.delegate( '.paginator a', 'click', self.paging );

      moduleActivity.delegate( 'a:not([href^=javascript],[onclick])', 'click', self.display );

      return function( name, options, cb ) {
        if( !(name in self.models) ) { self.models[name] = { _meta: {} }; }
        var model = self.models[name];
        model = $.extend( {}, options, model );

        model.open = function( evt ) {
          evt.preventDefault();

          var meta = model._meta;

          if( !meta.base_href ) {
            meta.base_href = $( this ).attr( 'href' );
          }

          if( !meta.add_href ) {
            meta.add_href = $( this ).attr( 'href' ) + 'add/';
          }

          if( !meta.list_href ) {
            meta.list_href = $( this ).attr( 'href' );
          }

          if( !meta.label && meta.label !== '' ) {
            meta.label = $( this ).text();
          }

          meta.current_href = meta.add_href;
          model.register();

          // Initial
          $.when( self.fetchTemplate( self.template ), $.get( meta.add_href ), $.get( meta.list_href ) ).then(
            function( template, edit, list ) {
              var view = {
                template: template
              , label: meta.label
              , edit: $( edit[0] ).find( '#content-main' ).html()
              , list: $( list[0] ).find( '#content-main' ).html()
              };

              self.render( Mustache.to_html( template, view ) );
            }
          );

          sidebar.show();

          return false;
        };

        model.register = function( id ) {
          self._active = model;

          if( id ) {
            $.get( '/curator/templates/' + name, function( data ) {
              return def.resolve( data );
            });
          }
        };

        cb && cb.call( self, model );

        model.dom.bind( 'click', model.open );
        return self;
      };
    //}( managepane );
    };

    instances_select.bind( 'change', function( evt ) {
      $.get( '/curator/instance/' + this.value, function( evt ) {
        location.reload( true );
      });
    });

    // Handle flagged
    //ajaxModel( 'flagged', { dom: flagged }, function( model ) {
    //  var self = this;

    //  model.open = function( evt ) {
    //    evt.preventDefault();

    //    var meta = model._meta;
    //    meta.label = 'Manage recently flagged';

    //    $.when( self.fetchTemplate( self.template ), self.fetchTemplate( self.table ), $.getJSON( '/curator/all_flagged/' ) ).then(
    //      function( template, table, flagged ) {
    //        var view = {
    //         template: template
    //        , label: meta.label
    //        };

    //        var dataView = {};
    //        dataView.headers = ['count', 'label'];
    //        
    //        $.each( flagged[0], function( i, row ) { row.index = i+1; });
    //        dataView.values = flagged[0];

    //        var table = Mustache.to_html( table, dataView );
    //        view.list = table;

    //        self.render( Mustache.to_html( template, view ) );

    //        model.display = function( evt ) {
    //          evt.preventDefault();

    //          var href = $( this ).attr( 'href' )
    //            , meta = self.normalizeMeta( href );

    //          meta.current_href = href + '/';
    //          var req = $.get( meta.current_href );

    //          $.when( self.fetchTemplate( self.template ), req, $.get( meta.list_href ) ).then(
    //            function( template, edit, list ) {
    //              var view = {
    //                template: template[0]
    //              , label: meta.label
    //              , edit: $( edit[0] ).find( '#content-main' ).html()
    //              , list: $( '#result_list' ).parent().html()
    //              };

    //              self.render( Mustache.to_html( template, view ) );

    //              self.sidebar.find( 'form' ).attr( 'action', meta.current_href )
    //                .find( '.deletelink' ).attr( 'href', href + '/delete/' );

    //              $( '#result_list' ).delegate( 'a:not([href^=javascript])', 'click', model.display );
    //            }
    //          );

    //          return false;
    //        };

    //        $( '#result_list' ).delegate( 'a:not([href^=javascript])', 'click', model.display );

    //        self.sidebar.show();

    //        return false;
    //    });
    //  };
    //});

    $.getJSON( '/curator/instances/', function( data ) {
      instances_select.empty();
      
      var i = 0;
      $.each( data, function( index, instance ) {
         var option = $( '<option/>' );
         if( instance.selected )  {
           option.attr( 'selected', 'selected' );
           i++;
         }

         option.val( instance.id ).text( instance.region );

         instances_select.append( option );
      });
    });
});
