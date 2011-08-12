This document describes the basic uses of how to use mapit. 

Every time that google maps is used the following needs to be imnported:
 
from gmapsfield.fields import GoogleMapsField

To define the model with a GoogleMapsField the declaration is:
map = GoogleMapsField()

It takes all of the same arguments including a default. See the documentation in the project for more information.
This isn't really used at all. 

To have a map in the form declare a variable map as follows:
map = GoogleMapsField().formfield()

The formfield() can take options for the form field, and this method is required in the form document. 
If this is not added (a common mistake), nothing will display in the web page. 

There can only be one map declared per form. It must be named "map" because this is what is inserted by the mapit.js.
This way you can also do a clean like so:

def clean_map(self):
    map = self.cleaned_data.get('map')
    if not map:
        raise forms.ValidationError("The map doesn't exist")
    mapDict = simplejson.loads(map)
    if len(mapDict["markers"]) == 0:
        raise forms.ValidationError("Please select a point on the map")
    return map

The html requires a script tag in the body block. This is basically what every page that has a map needs. 

    <script src="http://maps.google.com/maps/api/js?sensor=false&libraries=places" type="text/javascript"></script>
    <script type="text/javascript" src="/admin/gmapsfield/admin/admin.js"></script>
    <script src="{{MEDIA_URL}}js/games/mapit.js" type="text/javascript" charset="utf-8"></script>
    <script src="{{MEDIA_URL}}3pty/js/date.js" type="text/javascript" charset="utf-8"></script>
    <script>
        $(".google-map").mapit({{location|safe|escape}});
        $(".remove-map").remove();
    </script>

There needs to be a div tag with the class "google-map". This also takes a required argument data-type
which will always have a type of "Point". For example:

<div id="map" class="google-map" data-type="Point"/>

The id does not actually matter but because the JSON object "map" is returned in the post,
it sort of makes sense to only name it map. 

The map will also take a maximum number of points allowed on the map and a set of default points. If
default points are used, they do count toward the maximum points however an unlimited number can be
used. For example, if the maximum number of points allowed is 10, but there are 15 initial points,
the 15 will be plotted but the user will not be allowed to add any points and can only rearrange the
current points that exist. A maximum number is not required but if one is used it is defined as:

<input type="hidden" id="max_points_input" name="max_points_input" value="1">

The way that the initial points are defined is:
<input type="hidden" id="init_coordsX" name="init_coordsX" lat="LAT" lon="LON"/>
where X is (0, ...) and must start at 0. If the k'th value is skipped between 0 and N, it will stop plotting
at k-1. LAT is the latitude to plot the point, LON is the longetude to plot the point. 


