var uploadField = document.getElementById("id_profilFoto");

uploadField.onchange = function () {
    if (this.files[0].size > 1048576) {
        alert("Lütfen Maksimum 1MB boyutunda fotoğraf yükleyin.");
        this.value = "";
    }
};

$(document).ready(function () {

    $("#photo-open-div").click(function () {
        $("#photo-open-div").hide();
        $("#photo").slideDown();
    });
});

function try_photo() {
    select = document.getElementById('choose-photo');
    photo = document.getElementById('user-photo');

    select_value = select.options[select.selectedIndex].value;

    if (select_value == "1") {
        select_value = '/media/default_avatars/avatar.jpg';
    } else if (select_value == "2") {
        select_value = '/media/default_avatars/javier.jpg';
    } else if (select_value == "3") {
        select_value = '/media/default_avatars/joker.png';
    } else if (select_value == "4") {
        select_value = '/media/default_avatars/pennywise.jpg';
    } else if (select_value == "5") {
        select_value = '/media/default_avatars/scarface.jpg';
    } else if (select_value == "6") {
        select_value = '/media/default_avatars/unknown.jpg';
    } else if (select_value == "7") {
        select_value = '/media/default_avatars/yoda.jpg';
    }

    photo.src = select_value;
}