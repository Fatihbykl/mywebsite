$(document).ready(function () {
    var status = false;
    $('#sidebar-button').click(function () {
        if (status) {
            $('#sidebar').animate({left: '-250px'}, "swing");
            status = false;
        } else {
            $('#sidebar').animate({left: '0'}, "swing");
            status = true;
        }
    });

    $('#close-sidebar').click(function () {
        $('#sidebar').animate({left: '-250px'}, "swing");
        status = false;
    });
});

$(document).ready(function () {
    $('#go').keypress(function (event) {
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if (keycode == '13') {
            var input = document.getElementById('go').value;
            window.location.href = '?page=' + input;
        }
    });
});

