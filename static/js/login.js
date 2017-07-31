function compareLoginData() {
    var loginButton = $('#bt_login');
    var loginForm = $(".login");
    var enterLogin = $('#login_button');
    var counter = 0;

    loginButton.on('click', function() {
        counter ++;

        if (counter % 2 == 1) {
            loginForm.show(600);
        } else {
            loginForm.hide(600);
        }

        enterLogin.on('click', function() {
            counter ++;
            var username = $('#login-username');
            var password = $('#login-password');

            $.ajax({
                method: "POST", 
                url: "/login",
                data: {
                    username: username.val(),
                    password: password.val()
                },
                success: function(){
                    console.log(username.val());
                    console.log(password.val());
                }
            });
            loginForm.hide(600);

            var usernameFromCookie = Cookies.get('session');
            console.log(usernameFromCookie);
        });
        
    });
}


function main() {
    compareLoginData();
}

$(document).ready(main);