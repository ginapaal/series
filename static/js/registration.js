function registration() {
    var regButton = $('#bt_register');
    var regForm = $('.signup');
    var submitButton = $('#submit_button');
    counter = 0;

    regButton.on('click', function(){
        counter ++;

        if (counter % 2 === 1) {
            regForm.show(600);
        } else {
            regForm.hide(600);
        }

    });


    submitButton.on('click', function(){
        counter ++;
        var name = $('input[id="name"]');
        var email = $('input[id="email"]');
        var username = $('input[id="username"]');
        var password = $('input[id="password"]');
        var confirmPw = $('input[id="confirm"]');

     
        if (password.val() !== confirmPw.val()) {
            alert("Passwords don't match. Try again!");
            password.val('');
            confirmPw.val('');
        } else {
            $.ajax({
                method: "POST",
                url: "/registration", 
                data:{
                    name: name.val(),
                    email: email.val(),
                    username: username.val(),
                    password: password.val(),
                    confirm: confirmPw.val()
                },
                success: function(){
                    alert("New user registered.");
                }
            });
            regForm.hide(600);

            name.val("");
            email.val("");
            username.val("");
            password.val("");
            confirmPw.val("");
        }


    });
}

function main() {
    registration();
}

$(document).ready(main);