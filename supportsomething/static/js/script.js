$(document).ready(function () {

    if ($('#map_canvas').length > 0) {
        $('#map_canvas').height($(window).height() + 'px');
        $('#stream_canvas').height($(window).height() + 'px');
        $(window).resize(function () {
            $('#map_canvas').height($(window).height() + 'px')
            $('#stream_canvas').height($(window).height() + 'px')
        });

        var myLatlng = new google.maps.LatLng(34.1564768, -118.4561);

        var myOptions = {
            center:myLatlng,
            zoom:14,
            mapTypeId:google.maps.MapTypeId.ROADMAP
        };
        var map = new google.maps.Map(document.getElementById("map_canvas"),
                myOptions);

        var marker = new google.maps.Marker({
            position:myLatlng,
            title:"Hello World!"
        });

    }

    if ($('#upload').length > 0) {
        console.log('uploader');
        var uploader = new plupload.Uploader({
            runtimes:'html5,html4',
            browse_button:'upload',
            max_file_size:'5mb',
            url:'/upload_image',
            filters:[
                {title:"Image files", extensions:"jpg,gif,png"}
            ]
        });

        uploader.bind('QueueChanged', function () {
            uploader.start();
            //$('.uploader').attr('src', '/static/img/ajax-loader.gif');
        });
        uploader.bind('FileUploaded', function (uploader, file, response) {
            //$('.uploader').attr('src', response.response);
            var img = '<img src="' + response.response + '" />'
            var li = '<li>' + img + '</li>'
            $('.stream li:first').before(li);
        });

        uploader.bind('Error', function (uploader, error) {
            var message = error.message;
            if (console && console.log) {
                console.log(message);
            }
        });
        uploader.init();
    }
//    function valid_position(position) {
//        return position.coords.accuracy < 100 &&
//        (((new Date()).getTime() - position.timestamp) < 600000);
//    }
//
//    function set_current_location(position) {
//        if (valid_position(position)) {
//            console.log(position);
//            var myLatlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
//
//            var myOptions = {
//                center: myLatlng,
//                zoom: 14,
//                mapTypeId: google.maps.MapTypeId.ROADMAP
//            };
//            var map = new google.maps.Map(document.getElementById("map_canvas"),
//                myOptions);
//
//            var marker = new google.maps.Marker({
//                position: myLatlng,
//                title:"Hello World!"
//            });
//
//            marker.setMap(map);
//            navigator.geolocation.clearWatch(watchId);
//        }
//    }
//
//    function get_current_position_error() {
//
//    }
//
//    var watchId;
//    if (navigator.geolocation) {
//        watchId = navigator.geolocation.watchPosition(
//            set_current_location, get_current_position_error, {
//                enableHighAccuracy:true,
//                maximumAge:30000
//            });
//    } else {
//        error()
//    }
})
;