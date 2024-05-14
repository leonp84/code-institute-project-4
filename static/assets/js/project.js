if (window.localStorage.getItem('currentTheme') == 'dark') {
    toggleTheme()
}

$(function() {

    // Check for Theme Toggle
    $('#toggle-theme').on('click', function() {
        $('body').toggleClass('dark')
        $('.theme-switch').toggleClass('bg-dark');
        if ($('html').attr('data-bs-theme') == 'light') {
            $('html').attr('data-bs-theme', 'dark')
            window.localStorage.setItem('currentTheme', 'dark')
            $('.form-switch .form-check-input').css('background-position', 'right center')


        } else {
            $('html').attr('data-bs-theme', 'light')
            window.localStorage.setItem('currentTheme', 'light')
            $('.form-switch .form-check-input').css('background-position', 'left center')


        }
        $('#logo-light').toggle()
        $('#logo-dark').toggle()
    })

    // Update Account Form Visuals (if present)
    if ($('#signup_form')) {
    $('#signup_form').find('#id_email').attr('placeholder', 'Email (optional)')
    $('#reset-password').find('button').addClass('btn btn-outline-primary')
    }

    // Update Footer Copyright Date
    let now = new Date();
    $('#footer-date').text(now.getFullYear())
})


function toggleTheme() {
    $('body').toggleClass('dark')
    $('.theme-switch').toggleClass('bg-dark');
    if ($('html').attr('data-bs-theme') == 'light') {
        $('html').attr('data-bs-theme', 'dark')
        $('.form-switch .form-check-input').css('background-position', 'right center')
    } else {
        $('html').attr('data-bs-theme', 'light')
        $('.form-switch .form-check-input').css('background-position', 'left center')
    }
    $('#logo-light').toggle()
    $('#logo-dark').toggle()
}