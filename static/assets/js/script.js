if (window.localStorage.getItem('currentTheme') == 'dark') {
    toggleTheme()
}

$(function () {

    IdCounter = 2

    $('#add-new-subtask').on('click', function () {
        $('#subtask-container').append(extraTask(IdCounter))
        IdCounter++
        $('.delete-subtask').on('click', function () {
            $(this).parent().remove()
            addEventListener()
        })
    })    

    $('.form-check-input').on('click', function() {
        $(this).next().toggleClass('strikethrough')
    })

    // Theme Toggle Function
    $('#toggle-theme').on('click', function() {
        $('body').toggleClass('dark')
        $('.theme-switch').toggleClass('bg-dark');
        if ($('html').attr('data-bs-theme') == 'light') {
            $('html').attr('data-bs-theme', 'dark')
            window.localStorage.currentTheme = 'dark'
            window.localStorage.setItem('currentTheme', 'dark')


        } else {
            $('html').attr('data-bs-theme', 'light')
            window.localStorage.setItem('currentTheme', 'light')

        }
        $('#logo-light').toggle()
        $('#logo-dark').toggle()
        console.log(window.localStorage.getItem('currentTheme'))
    })

    addEventListener()


    // Updating DOM Progress Bar Visuals due to HTML Linter giving errors with Python Templating Language
    let progressBars = document.getElementsByClassName('progress-bar');
    for (let i = 0; i < progressBars.length; i++) {
        newValue = progressBars[i].getAttribute('aria-valuenow')
        progressBars[i].setAttribute('style', `width: ${newValue}%`)
    }
})

function toggleTheme() {
    $('body').toggleClass('dark')
    $('.theme-switch').toggleClass('bg-dark');
    if ($('html').attr('data-bs-theme') == 'light') {
        $('html').attr('data-bs-theme', 'dark')
    } else {
        $('html').attr('data-bs-theme', 'light')

    }
    $('#logo-light').toggle()
    $('#logo-dark').toggle()
    console.log('test')
}

function extraTask(num) {
    return `
    <div id="subtasks" class="input-group flex-nowrap">
        <span class="input-group-text delete-subtask" id="delete-subtask-{{ num }}">X</span>
        <input type="text" name="subtasks" class="form-control" placeholder="Subtask ..."
            aria-label="Subtask" aria-describedby="delete-subtask-{{ num }}">
    </div>
    `
}

function addEventListener() {
    $('.delete-subtask').on('click', function () {
        $(this).parent().remove()
    })
}