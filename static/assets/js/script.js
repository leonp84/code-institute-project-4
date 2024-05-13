if (window.localStorage.getItem('currentTheme') == 'dark') {
    toggleTheme()
}

$(function () {

    $('#signup_form').find('#id_email').attr('placeholder', 'Email (optional)')
    $('#reset-password').find('button').addClass('btn btn-outline-primary')

    IdCounter = 2

    $('#add-new-subtask').on('click', function () {
        $('#subtask-container').append(extraTask(IdCounter))

        $('input[name="subtasks"]').focus()


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

    })

    addEventListener()
    checkTaskNameDuplicates()


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
}

function extraTask(num) {
    return `
    <div class="input-group flex-nowrap mt-1">
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


function checkTaskNameDuplicates() {
    let currentTasks = []
    saved_tasks = document.getElementsByClassName('task-title')
    for (i = 0; i < saved_tasks.length; i++) {
        currentTasks.push(saved_tasks[i].innerText)
    }
    console.log(currentTasks)

    let errorState = false
    document.getElementById('new-task-title').addEventListener('keydown', function(e) {

        // Take care of Backpsace character
        user_input = this.value + e.key
        if (e.key == 'Backspace') { 
            user_input = this.value.slice(0,-1)
        }

        if (currentTasks.includes(user_input)) {
            $('#new-task-title').css('border', '2px solid red')
            $('#new-task-title').next().text('A Task with that name already exists')
            $('#new-task-title').next().css('color', 'red')
            $('#new-task-title').next().css('text-decoration', 'none')
            $('#submit-new-task').addClass('disabled')
            errorState = true
        } else {
            if (errorState) {
                $('#new-task-title').css('border', '1px solid #dee2e6')
                $('#new-task-title').next().text('Title')
                $('#new-task-title').next().css('color', 'rgb(186, 185, 185)')
                $('#new-task-title').next().css('text-decoration', 'underline')
                $('#submit-new-task').removeClass('disabled')
                errorState = false
            }
        }
    })
    
}