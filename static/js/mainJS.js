$(document).ready(function() {
    $(".container").fadeIn();

    $(".reveal_password_click").click(function(e) {
        let s = event.target.getAttribute("data-target");
        $('.real_password > div').html(`<p class="my-5">Your password is ${s}</p>`);
        $('.real_password').fadeIn();
    });

    $(".reveal_password_button").click(function(e) {
        let s = event.target.getAttribute("data-target");
        $('.real_password > div').html(`<p class="my-5">Your password is ${s}</p>`);
        $('.real_password').fadeIn();
    });

    $('.close_button').click(function (e) {
        $('.real_password').fadeOut(1000);
    })
})
