$(function () {

    // Implementing Drag and Drop

    // Add & remove opacity to picked dragged item
    dragItems = document.getElementsByClassName('task')
    for (i = 0; i < dragItems.length; i++) {
        dragItems[i].addEventListener('dragstart', function() {
            $(this).addClass('dragging')
        })
        dragItems[i].addEventListener('dragend', function() {
            $(this).removeClass('dragging')

            // Send Ajax request to Python backend with task name and new column title
            taskName = ($(this).find('.task-title').first().text())
            newColumn = ($(this).parent().find('#column-title').text())

            $.ajax({
                url: "/update_status/",
                type: "POST",
                dataType: "json",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": CSRF_TOKEN, 
                    'task': taskName,
                    'column': newColumn,
                },
                success: function(response) {
                    console.log(response.message);
                },
                error: function(xhr, status, error) {
                    console.error("Error:", error);
                }
            });

        })
    }

    // Append dragged item to the end of dragover container
    dropZones = document.getElementsByClassName('column')
    for (i = 0; i < dropZones.length; i++) { 
        dropZones[i].addEventListener('dragover', function(e) {
            e.preventDefault()
            let draggedItem = document.getElementsByClassName('dragging')[0]
            this.append(draggedItem)
        })
    }



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

    $('#search-icon').on('click', function() {
        $('#search-box').toggle()
        $('#search-box').find('input').focus()
    })

    addEventListener()
    checkTaskNameDuplicates()


    // Updating DOM Progress Bar Visuals to avoid linting issues
    let progressBars = document.getElementsByClassName('progress-bar');
    for (let i = 0; i < progressBars.length; i++) {
        newValue = progressBars[i].getAttribute('aria-valuenow')
        progressBars[i].setAttribute('style', `width: ${newValue}%`)
    }
})

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

    let errorState = false
    document.getElementById('new-task-title').addEventListener('keydown', function(e) {

        // Take care of Backpsace character
        user_input = this.value + e.key
        if (e.key == 'Backspace') { 
            user_input = this.value.slice(0,-1)
        }

        if (user_input.length > 100) {
            e.preventDefault()
        } else {
            // Update Character Count with Task Title Creation
            $('#char-count').text(100 - user_input.length)
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