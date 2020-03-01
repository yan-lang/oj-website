(function () {
    'use strict';
    window.addEventListener('load', function () {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);

    const password2 = document.getElementById('id_new_password2');
    const password = document.getElementById('id_new_password1');
    password2.addEventListener("input", function (event) {
        matchPasswords();
    });

    password.addEventListener("input", function (event) {
        if (password2.value !== "") matchPasswords();

        // https://www.cnblogs.com/yanglang/p/11468318.html
        const regx = new RegExp('(?=.*[0-9])(?=.*[a-zA-Z]).{8,20}');
        if (!regx.test(password.value)) {
            password.classList.add('is-invalid');
            password.setCustomValidity("Your password must be 8-20 characters long and contain both letters and numbers.");
        } else {
            password.classList.remove('is-invalid');
            password.setCustomValidity("");
        }
    });

    function matchPasswords() {
        if (password.value === password2.value) {
            password2.classList.remove("is-invalid");
            password2.setCustomValidity("");
        } else {
            password2.classList.add("is-invalid");
            password2.setCustomValidity("Password did not match.");
        }
    }

})();

// https://stackoverflow.com/questions/45938703/cant-make-the-validation-work-in-bootstrap-4
// https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation
// http://bootstrap-show-password.wenzhixin.net.cn/examples/#basic.html