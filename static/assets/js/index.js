$(function () {

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

    // Implementing Drag and Drop

    // Add & remove opacity to picked dragged item
    dragItems = document.getElementsByClassName('task')
    for (i = 0; i < dragItems.length; i++) {
        dragItems[i].addEventListener('dragstart', function() {
            $(this).addClass('dragging')
        })
        dragItems[i].addEventListener('dragend', function() {
            $(this).removeClass('dragging')

            newColumnName = ($(this).parent().find('.column-title').text())
            newColumnId = ($(this).parent().find('.column-id').text())
            lastColumnName = ($('.column').last().find('.column-title').text())
            taskId = $(this).find('.task-id').text()
            console.log(newColumnName)
            console.log(newColumnId)
            console.log(lastColumnName)

            // Update Visuals after task lands in new column
            if (newColumnName === lastColumnName) {
                $(this).find('.task-completed-check').show()
                $('body').find(`#completed-check-${taskId}`).show()
            }  else {
                $(this).find('.task-completed-check').hide()
                $('body').find(`#completed-check-${taskId}`).hide()

            }
            editStatus = $('body').find(`#select-status-${taskId}`).find('option')
            for (i = 0; i < editStatus.length; i++) {
                editStatus[i].removeAttribute('selected')
            }
            for (i = 0; i < editStatus.length; i++) {
                if (editStatus[i].value == newColumnId) {
                    editStatus[i].setAttribute('selected', '')
                } 
            }
            console.log($('body').find(`#select-status-${taskId}`).html())




            // Send Ajax request to Python backend with task names and new column title
            // $(this).parent().find('.task-title').text()
            let tasksInColumn = [];
            $(this).parent().find('.task-title').each(function(){
                tasksInColumn.push($(this).text());
            })

            $.ajax({
                url: "/update_status/",
                type: "POST",
                data: JSON.stringify({ 'newColumnName': newColumnName, 
                                       'tasksInColumn': tasksInColumn  }),
                dataType: "json",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": CSRF_TOKEN, 
                },
                success: function(response) {
                    // console.log(response.message);
                },
                error: function(xhr, status, error) {
                    // console.error("Error:", error);
                }
            });

        })
    }

    // Append dragged item to the end of dragover container
    dropZones = document.getElementsByClassName('column')
    for (i = 0; i < dropZones.length; i++) { 
        dropZones[i].addEventListener('dragover', function(e) {
            e.preventDefault()
            let closestTask = getClosestTask(this, e.clientY)
            let draggedItem = document.getElementsByClassName('dragging')[0]


            if (closestTask == null) {
                this.append(draggedItem)
            } else {
                this.insertBefore(draggedItem, closestTask)
            }
        })
    }
})

function getClosestTask(column, mouseY) {

    // Get all Tasks in current column that are not being dragged
    let tasksInColumn = [];
    $(column).find('.task').each(function(){
        if (!$(this).hasClass('dragging')) {
        tasksInColumn.push(this);
    }
    })

    return tasksInColumn.reduce((closest, child) => {
        // Get horizontal and vertical heights of tasks divs
        let taskBox = child.getBoundingClientRect()
        // Set mouse offset below zero when above middle of task div
        let offset = mouseY - taskBox.top - taskBox.height / 2
        // Reduce down to closest task (offset closest to zero)
        if (offset < 0 && offset > closest.offset) {
          return { offset: offset, element: child }
        } else {
          return closest
        }
      }, { offset: Number.NEGATIVE_INFINITY }).element

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