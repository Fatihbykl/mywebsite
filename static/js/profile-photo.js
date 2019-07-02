var uploadField = document.getElementById("id_profilFoto");

uploadField.onchange = function () {
    if (this.files[0].size > 1048576) {
        alert("Lütfen Maksimum 1MB boyutunda fotoğraf yükleyin.");
        this.value = "";
    }
};
