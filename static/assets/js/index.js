$(function () {

    // Update 'Add Task' Button content when form submitted
    $('#add-new-task-form').on('submit', function() {
        $('#submit-new-task').html(
        `<span>Adding...</span>
        <div class="spinner-border spinner-border-sm" role="status"></div>`);
        $('#submit-new-task').attr('disabled', true);
        $('#submit-new-task').css('background-color', 'grey');
    });

    $('.edit-task-form').on('submit', function() {
        $('.update-task-submit').html(
        `<span>Updating...</span>
        <div class="spinner-border spinner-border-sm" role="status"></div>`);
        $('.update-task-submit').attr('disabled', true);
        $('.update-task-submit').css('background-color', 'grey');
    });

    // Auto close Alerts after Task & Board Model CRUD
    async function updateAlertDismissal() {
        if('.alert') {
            let sleepNow = (delay) => new Promise((resolve) => setTimeout(resolve, delay));
            for (let i = 180; i >= 0; i--) {
                $('.alert').find('.progress-bar').css('width', i);
                $('.alert').find('.progress-bar').attr('aria-valuenow', i);
                await sleepNow(30);
                }
            $('.alert').hide();
            }
        
        }
        
    updateAlertDismissal();
    // Populate new Subtask input on add task Modal
    let IdCounter = 2;
    $('#add-new-subtask').on('click', function () {
        $('#subtask-container').append(extraTask(IdCounter));
        $('input[name="subtasks"]').focus();
        IdCounter++;
        addEventListener();
    });

    // Add text strikethrough when subtasks checked on edit task Modal
    $('.form-check-input').on('click', function () {
        $(this).next().toggleClass('strikethrough');
    });
    
    // Eventlistener for search icon to reveal search bar
    $('#search-icon').on('click', function () {
        $('#search-box').toggle();
        $('#search-box').find('input').focus();
    });

    addEventListener();
    checkTaskNameDuplicates();

    // Updating DOM Progress Bar Visuals to avoid linting issues
    let progressBars = document.getElementsByClassName('progress-bar');
    for (let i = 0; i < progressBars.length; i++) {
        let newValue = progressBars[i].getAttribute('aria-valuenow');
        progressBars[i].setAttribute('style', `width: ${newValue}%`);
    }

    // Implementing Drag and Drop
    let dragItems = document.getElementsByClassName('task');
    for (let i = 0; i < dragItems.length; i++) {
        dragItems[i].addEventListener('dragstart', function () {
            $(this).addClass('dragging');
        });
        dragItems[i].addEventListener('dragend', function () {
            $(this).removeClass('dragging');

            let newColumnName = $(this).parent().find('.column-title').text();
            let newColumnId = $(this).parent().find('.column-id').text();
            let lastColumnName = $('.column').last().find('.column-title').text();
            let taskId = $(this).find('.task-id').text();

            // Update Visuals after task lands in new column
            if (newColumnName === lastColumnName) {
                $(this).find('.task-completed-check').show();
                $(`#completed-check-${taskId}`).show();
            } else {
                $(this).find('.task-completed-check').hide();
                $(`#completed-check-${taskId}`).hide();
            }
            
            // Update Task detail (new column) on modal, when task moved
            let editStatus = $(`#select-status-${taskId}`).find('option');
            for (let i = 0; i < editStatus.length; i++) {
                editStatus[i].removeAttribute('selected');
            }
            for (let i = 0; i < editStatus.length; i++) {
                if (editStatus[i].value == newColumnId) {
                    editStatus[i].setAttribute('selected', '');
                }
            }

            // Send Ajax request to Python backend with task names and new column title
            let tasksInColumn = [];
            $(this).parent().find('.task-id').each(function () {
                tasksInColumn.push($(this).text());
            });

            // The CSFR_TOKEN variable below is provided at the bottom of the respective HTML file
            $.ajax({
                url: "/update_status/",
                type: "POST",
                data: JSON.stringify({
                    'newColumnId': newColumnId,
                    'tasksInColumn': tasksInColumn
                }),
                dataType: "json",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": CSRF_TOKEN,
                },
                success: function (response) {
                    console.log(response.message);
                },
                error: function (xhr, status, error) {
                    console.error("Error:", error);
                }
            });

        });
    }

    // Allow for drag and drop sorting within columns
    let dropZones = document.getElementsByClassName('column');
    for (let i = 0; i < dropZones.length; i++) {
        dropZones[i].addEventListener('dragover', function (e) {
            e.preventDefault();
            let closestTask = getClosestTask(this, e.clientY);
            let draggedItem = document.getElementsByClassName('dragging')[0];

            if (closestTask == null) {
                this.append(draggedItem);
            } else {
                this.insertBefore(draggedItem, closestTask);
            }
        });
    }
});

function getClosestTask(column, mouseY) {
    /**
     * Reduce function to get closest task to dragged task
     */
    let tasksInColumn = [];
    $(column).find('.task').each(function () {
        if (!$(this).hasClass('dragging')) {
            tasksInColumn.push(this);
        }
    });

    return tasksInColumn.reduce((closest, child) => {
        // Get horizontal and vertical heights of tasks divs
        let taskBox = child.getBoundingClientRect();
        // Set mouse offset below zero when above middle of task div
        let offset = mouseY - taskBox.top - taskBox.height / 2;
        // Reduce down to closest task (offset closest to zero)
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;

}

function extraTask(num) {
    /**
     * Populate new subtask input on add task modal
     */
    return `
    <div class="input-group flex-nowrap mt-1">
        <span class="input-group-text delete-subtask" id="delete-subtask-${num}">X</span>
        <input type="text" name="subtasks" class="form-control" placeholder="Subtask ..."
            aria-label="Subtask" aria-describedby="delete-subtask-${num}">
    </div>
    `;
}

function addEventListener() {
    /**
     * Eventlistener for deleting subtasks
     */
    $('.delete-subtask').on('click', function () {
        $(this).parent().remove();
    });
}

function checkTaskNameDuplicates() {
    /**
     * Block users from entering duplicate Task names
     */
    let currentTasks = [];
    let saved_tasks = document.getElementsByClassName('task-title');
    for (let i = 0; i < saved_tasks.length; i++) {
        currentTasks.push(saved_tasks[i].innerText);
    }

    let errorState = false;
    document.getElementById('new-task-title').addEventListener('keydown', function (e) {

        // Handle Backspace character
        let user_input = this.value + e.key;
        if (e.key == 'Backspace') {
            user_input = this.value.slice(0, -1);
        }

        if (user_input.length > 100) {
            e.preventDefault();
        } else {
            // Update Character Count with Task Title Creation
            $('#char-count').text(100 - user_input.length);
        }

        if (currentTasks.includes(user_input)) {
            $('#new-task-title').css('border', '2px solid red');
            $('#new-task-title').next().text('A Task with that name already exists');
            $('#new-task-title').next().css('color', 'red');
            $('#new-task-title').next().css('text-decoration', 'none');
            $('#submit-new-task').addClass('disabled');
            errorState = true;
        } else {
            if (errorState) {
                $('#new-task-title').css('border', '1px solid #dee2e6');
                $('#new-task-title').next().text('Title');
                $('#new-task-title').next().css('color', 'rgb(186, 185, 185)');
                $('#new-task-title').next().css('text-decoration', 'underline');
                $('#submit-new-task').removeClass('disabled');
                errorState = false;
            }
        }
    });
}
