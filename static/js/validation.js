function validate_email() {
    var msg = document.getElementById('message-email');
    var email = document.getElementById('id_email');
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    if (!re.test(email.value)) {
        msg.innerHTML = "Lütfen geçerli bir email girin."
    } else {
        msg.innerHTML = "";
    }
}

function validate_pass() {
    var pass1 = document.getElementById('id_password');
    var pass2 = document.getElementById('id_password_confirm');
    var msg = document.getElementById('message-pass')
    if (pass1.value.localeCompare(pass2.value)) {
        msg.innerHTML = "Şifreler eşleşmiyor."
    } else {
        msg.innerHTML = "";
    }
}

function validate_username_length() {
    var username = document.getElementById('id_username');
    var msg = document.getElementById('message-username');

    if (username.value.length < 8) {
        msg.innerHTML = "Kullanıcı adı en az 8 harf olmalı. ( " + username.value.length + " )";
    }
    else {
        msg.innerHTML = "";
    }
}
