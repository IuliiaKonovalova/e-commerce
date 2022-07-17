(function ($) {
    $.fn.miv = function (options) {
        var elemRef = $.extend({
            image: '.cam',
            video: '.vid'
        }, options);
        var i = 0;
        var j = 0;
        $(document).on('click', elemRef.image, function () {
            $(elemRef.image).after("<input type='file' id='imgupload" + i + "' style='display:none;' name='image[" + i + "]'/>");
            $('#imgupload' + i).trigger('click');
            $(document).on('change', '#imgupload' + i, function () {
                var file = $(this).get(0);
                var preview = window.URL.createObjectURL(file.files[0]);
                $('.gallery').append("<div class='apnd-img'><img src='" + preview + "' id='img" + i + "' class='img-responsive'><i class='fa fa-close delfile'></i></div>");
                i++
            })
        });
        $(document).on('click', elemRef.video, function () {
            $(elemRef.video).after("<input type='file' style='display:none;' id='vidupload" + j + "' name='video[" + j + "]'/>");
            $('#vidupload' + j).trigger('click');
            $(document).on('change', '#vidupload' + j, function () {
                var file = $(this).get(0);
                var preview = window.URL.createObjectURL(file.files[0]);
                $('.gallery').append("<div class='apnd-img'><iframe width='50' height='50' src='" + preview + "' id='vid" + j + "' frameborder='0' allowfullscreen></iframe><i class='fa fa-close delfile1'></i></div>");
                j++
            })
        });
        $(document).on('click', '.delfile', function () {
            var elem = $(this).prev().attr('id').substr(3, 4);
            $(this).parent().remove();
            $('#imgupload' + elem).remove()
        });
        $(document).on('click', '.delfile1', function () {
            var elem = $(this).prev().attr('id').substr(3, 4);
            $(this).parent().remove();
            $('#vidupload' + elem).remove()
        })
    }
}(jQuery))