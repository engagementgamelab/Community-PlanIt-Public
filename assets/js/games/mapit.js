(function(window, $) {

    $.fn.mapit = function(opts) {
        var markers = [], marker, line, map, _map, polygons = [], data = {}, type, state, infowindow,
            colors = ['#FF0000', '#00FF00', '#0000FF', '#FF8C00', '#F0F8FF', '#8B008B', '#FF0000'];

        opts = $.extend({
            coordinates: [0,0],
            zoom: 16,
            markers: [],
            add: ".add",
            rm: ".rm",
            submit: ".submit",
            autocomplete: []
        }, opts);

        function adjustMapBounds() {
            var markerCount = markers.length;
            if (markerCount > 0) {
                var bounds = new google.maps.LatLngBounds();
                for (var i = 0; i < markerCount; i++) {
                    bounds.extend(markers[i].position);
                }
                map.panToBounds(bounds);
                map.fitBounds(bounds);
            }
        }

        function updatePolygons(color, keep) {
            if(!keep) {
                $.each(polygons, function(index, obj) {
                    obj.setMap(null);
                    polygons.splice(index, 1);
                });
            }

            // Iterate markers array
            var positions = function() {
                var _internal = [];

                $.each(markers, function(index, obj) {
                    obj.fillColor = colors[color] || "#FF0000";
                    obj.fillOpacity = .8;
                    obj.getMap() !== null && _internal.push( obj.getPosition() );
                });

                return _internal;
            }();

            polygon = polygons[ polygons.push( new google.maps.Polygon({
                paths: positions,
                strokeColor: "#FFF000",
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: colors[color] || "#FF0000",
                fillOpacity: 0.35
            }) ) - 1];

            polygon.setMap(map);

            return polygon;
        }

        function update() {
            data.coordinates = [ map.center.lat(), map.center.lng() ];
            data.zoom = map.zoom;
            data.markers = [];
            data.type = type;

            $.each(markers, function() {
                var marker = { coordinates: [ this.position.lat(), this.position.lng() ] };
                data.markers.push(marker);
            });

            _map.attr("value", JSON.stringify(data));

            if(line && line.getPath()) {
                var path = line.getPath();
                path.clear();

                $.each(markers, function() {
                    path.push(this.position);
                });
            }
        }

        $(opts.add).bind("click", function() {
            var that = $(this);
            function refresh(marker) {
                line && line.setMap(null);

                if(type === 'Shape') {
                    updatePolygons();
                }
                else if(type === 'Line') {
                    var that = $(this);
                    line = new google.maps.Polyline({
                        strokeColor: '#FF0000',
                        strokeOpacity: 1.0,
                        strokeWeight: 2
                    });

                    line.setMap(map);
                }

                google.maps.event.addListener(marker, "dragend", function() {
                    update();
                    type === 'Shape' && updatePolygons();
                });

                update();
            }
                
            // Actions for Point/Line/Shape
            switch(type) {
                case 'Point':
                    maxPoints = -1;
                    input = document.getElementById("max_points_input");
                    if (input != null && input.value != "")
                        if (parseInt(input.value) != NaN)
                            maxPoints = parseInt(input.value);
                    
                    if (maxPoints > 0 && markers.length < maxPoints)
                    {
                        marker = new google.maps.Marker({
                            position: map.getCenter(),
                            draggable: draggable,
                            map: map
                        });
                        markers.push(marker);
                        for (x = 0; x < markers.length; x++)
                        {
                            refresh(markers[x]);
                        }
                    }

                    break;
                case 'Shape':
                    var ctr = map.getCenter(), mkr, lat, lng,
                        cenX = parseFloat(ctr.lat()),
                        cenY = parseFloat(ctr.lng()),
                        bounds = map.getBounds(),
                        sw = bounds.getSouthWest(),
                        ne = bounds.getNorthEast(),
                        latSpan = (parseFloat(ne.lat()) - parseFloat(sw.lat())) / 2,
                        lngSpan = (parseFloat(ne.lng()) - parseFloat(sw.lng())) / 2,
                        n = 5;
                        
                    for(var i=0; i<n; i++) {
                        lat = cenX + Math.sin((Math.PI*2)/n*i) * (latSpan * 0.5);//(cenX * 0.9);
                        lng = cenY + Math.cos((Math.PI*2)/n*i) * (lngSpan * 0.5);//(cenY * 0.9);

                        mkr = new google.maps.LatLng(lat, lng);

                        marker = new google.maps.Marker({
                            position: mkr,
                            draggable: true,
                            map: map
                        });
                        markers.push(marker);
                        refresh(marker);
                    }
                    that.attr("disabled", "disabled");

                    break;
                case 'Line':
                    marker = new google.maps.Marker({
                        position: map.getCenter(),
                        draggable: true,
                        map: map
                    });
                    markers.push(marker);
                    refresh(marker);

                    break;
            };


            return false;
        });

        $(opts.rm).bind("click", function() {
            for (x = 0; x < markers.length; x++)
            {
                markers[x].setMap(null);
            }
            markers = [];
            return false;
        });

        $(opts.submit).bind("click", function() {
            update();
        });
        
        return this.each(function() {
            var coordinates = new google.maps.LatLng(opts.coordinates[0], opts.coordinates[1]),
                bounds = new google.maps.LatLngBounds(),
                that = $(this);
            type = that.attr("data-type");
            state = that.attr("data-state");

            map = new google.maps.Map(this, {
                zoom: opts.zoom,
                disableDefaultUI: true,
                center: coordinates,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            });
            
            draggable = true;
            drag_elem = document.getElementById("dragable");
            if (drag_elem != null && drag_elem.value != "")
                if (drag_elem.value.toLowerCase() == "false")
                    draggable = false;
            
            var x = 0;
            var elem_str = "init_coords".concat(x);
            while (document.getElementById(elem_str) != null)
            {
                elem = document.getElementById(elem_str).attributes;
                lat = parseFloat(elem.lat.value);
                lon = parseFloat(elem.lon.value);
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(lat,lon),
                    draggable: draggable,
                    map: map
                });
                google.maps.event.addListener(marker, "dragend", function() {
                    update();
                    type === 'Shape' && updatePolygons();
                }); 
                marker.message = elem.message.value;
                marker.player = elem.player.value;
                markers.push(marker);
                
                x++;
                elem_str = "init_coords".concat(x)
            }
            
            var input = document.getElementById('google_search');
            if (input != null)
            {
                opts.autocomplete = new google.maps.places.Autocomplete(input);
                opts.autocomplete.bindTo('bounds', map)
                
                google.maps.event.addListener(opts.autocomplete, 'place_changed', function() {
                    maxPoints = parseInt(document.getElementById("max_points_input").value);
                    if (markers.length < maxPoints)
                    {
                        var place = opts.autocomplete.getPlace();
                        if (place.geometry.viewport) {
                          map.fitBounds(place.geometry.viewport);
                        } else {
                          map.setCenter(place.geometry.location);
                          map.setZoom(16);
                        }
                        var marker = new google.maps.Marker({
                            position: place.geometry.location,
                            draggable: true,
                            map: map
                        });
                        markers.push(marker);
                        var input = document.getElementById('google_search');
                        input.value = "";
                    }
                    return false;
                });
            }
            
            
            if(state === "played") {
                var marker_coordinates;
                if(type === "Point" && opts.markers && opts.markers.length) {
                    marker_coordinates = new google.maps.LatLng(opts.markers[0].coordinates[0], opts.markers[0].coordinates[1]),
                    marker = new google.maps.Marker({
                        position: marker_coordinates,
                        draggable: false,
                        map: map
                    });
                    markers.push(marker);
                }
                else if(type === "Shape" && opts.markers && opts.markers.length) {
                    $.each(opts.markers, function() {
                        var coord = new google.maps.LatLng(this.coordinates[0], this.coordinates[1]);
                        marker = new google.maps.Marker({
                            position: coord,
                            draggable: false,
                            map: map
                        });
                        markers.push(marker);
                    });
                    updatePolygons();
                }
                else if(type === 'Line' && opts.markers) {
                    line = new google.maps.Polyline({
                        strokeColor: '#FF0000',
                        strokeOpacity: 1.0,
                        strokeWeight: 2
                    });
                    line.setMap(map);

                    var path = line.getPath();
                    path.clear();

                    $.each(opts.markers, function() {
                        path.push(new google.maps.LatLng(this.coordinates[0], this.coordinates[1]));
                    });
                }
            }

            // Displays an overview of all markers points lines etc from games that have been previously
            // played.
            else if(state === 'overview') {
                if(type === "Point" && opts.markers && opts.markers.length) {
                    $.each(markers, function() {
                        this.draggable = false;

                        var message = this.message;
                        var player = this.player;

                        google.maps.event.addListener(this, 'click', function() {
                            if (infowindow){
                                infowindow.close()
                            }

                            infowindow = new google.maps.InfoWindow({
                                content:  '<div>' + message + '</div><div style="text-align:right;">&#8211; ' + player + '</div>'
                            });
                            
                            infowindow.open(map, this);
                        });
                    });
                }
                else if(type === "Shape" && opts.markers && opts.markers.length) {
                    var first_marker, shape;

                    // Iterate over each shape
                    $.each(opts.markers, function(i) {
                        markers = [];
                        var message = "", comment_count, url;

                        // Iterate over each point in the shape
                        $.each(this, function() {
                            var coord = new google.maps.LatLng(this.coordinates[0], this.coordinates[1]);
                            var marker = new google.maps.Marker({
                                position: coord,
                                draggable: false
                            });
                            markers.push(marker);
                        });

                        shape = updatePolygons(Math.floor(Math.random()*6), true);

                        // Close off this value
                        var placement = markers[0];

                        // Render out info window
                        google.maps.event.addListener(shape, 'click', function() {
                            // Use the first marker to extract information
                            first_marker = opts.markers[i][0];

                            if(infowindow) {
                                infowindow.close();
                            }

                            infowindow = new google.maps.InfoWindow({
                                content: first_marker.message + ' - ' + first_marker.player
                            });

                            infowindow.open(map, placement);
                        });
                    });
                }
                else if(type === 'Line' && opts.markers) {
                    var message = '', player = '';

                    // Iterate over each line
                    $.each(opts.markers, function() {
                        var message = '', player = '';
                        line = new google.maps.Polyline({
                            strokeColor: '#'+Math.floor(Math.random()*16777215).toString(16),
                            strokeOpacity: 1.0,
                            strokeWeight: 2
                        });
                        line.setMap(map);

                        var path = line.getPath();
                        path.clear();

                        // Iterate over the points of each line
                        $.each(this, function() {
                            var loc = new google.maps.LatLng(this.coordinates[0], this.coordinates[1]);
                            path.push(loc);

                            var marker = new google.maps.Marker({
                                position: loc,
                                draggable: false,
                                map: map
                            });
                            markers.push(marker);

                            if(message = this.message) {
                                player = this.player;

                                google.maps.event.addListener(marker, 'click', function() {
                                    if (infowindow){
                                        infowindow.close()
                                    }

                                    infowindow = new google.maps.InfoWindow({
                                        content: message + " - " + player
                                    });
                                        
                                    infowindow.open(map, marker);
                                });
                            }
                        });
                    });
                }
            }

            _map = $("<input type='hidden' name='map' value=''/>").insertAfter(this);
            try {
                update()
            }catch(err){
                alert(error)
            }
            adjustMapBounds();
        });

    };

})(this, this.jQuery);
