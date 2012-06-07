$(document).ready(function() {
    function valid_position(position) {
        return position.coords.accuracy < 100 &&
        (((new Date()).getTime() - position.timestamp) < 600000);
    }

    function set_current_location(position) {
        if (valid_position(position)) {
            console.log(position);
            var myLatlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

            var myOptions = {
                center: myLatlng,
                zoom: 14,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            var map = new google.maps.Map(document.getElementById("map_canvas"),
                myOptions);

            var marker = new google.maps.Marker({
                position: myLatlng,
                title:"Hello World!"
            });

            marker.setMap(map);
            navigator.geolocation.clearWatch(watchId);
        }
    }

    function get_current_position_error() {
        
    }
    
    var watchId;
    if (navigator.geolocation) {
        watchId = navigator.geolocation.watchPosition(
            set_current_location, get_current_position_error, {
                enableHighAccuracy:true,
                maximumAge:30000
            });
    } else {
        error()
    }
});