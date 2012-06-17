$(document).ready(function () {

    if ($('#map_canvas').length > 0) {
        $('#map_canvas').height($(window).height() + 'px');
        $('#stream_canvas').height($(window).height() + 'px');

        $(window).resize(function () {
            $('#map_canvas').height($(window).height() + 'px')
            $('#stream_canvas').height($(window).height() + 'px')
        });
    }

    if ($('.fb-login').length > 0) {
        $('.fb-login').click(function (e) {
            e.preventDefault();
            var w = 780;
            var h = 450;
            var l = (screen.width - w) / 2;
            var t = (screen.height - h) / 2;
            window.open('/login', 'auth', 'width=' + w + ',height=' + h + ',top=' + t + ',left=' + l);
        });

        window.onFacebookAuth = function () {
            location.reload();
        }

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
        marker.setMap(map);
    }

    if ($('#upload').length > 0) {
        uploader();
    }

    function uploader() {
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
            var img = '<img src="/static/img/ajax-loader.gif" />'
            var li = '<li>' + img + '</li>'
            $('.stream li:first').before(li);
            $('#upload i').removeClass('icon-upload');
            $('#upload i').addClass('icon-loading');
        });

        uploader.bind('FileUploaded', function (uploader, file, response) {
            $('.stream li:first img').attr('src', response.response);
            $('#upload i').addClass('icon-upload');
            $('#upload i').removeClass('icon-loading');
        });

        uploader.bind('Error', function (uploader, error) {
            var message = error.message;
            if (console && console.log) {
                console.log(message);
            }
        });
        uploader.init();
    }
});