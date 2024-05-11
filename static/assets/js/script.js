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

   
    addEventListener()


    // Updating DOM Progress Bar Visuals due to HTML Linter giving errors with Python Templating Language
    let progressBars = document.getElementsByClassName('progress-bar');
    for (let i = 0; i < progressBars.length; i++) {
        newValue = progressBars[i].getAttribute('aria-valuenow')
        progressBars[i].setAttribute('style', `width: ${newValue}%`)
    }
})



function extraTask(num) {
    return `
    <div id="subtasks" class="input-group flex-nowrap">
        <span class="input-group-text bg-dark text-white delete-subtask" id="delete-subtask-{{ num }}">X</span>
        <input type="text" name="subtasks" class="form-control bg-transparent text-white" placeholder="Subtask ..."
            aria-label="Subtask" aria-describedby="delete-subtask-{{ num }}">
    </div>
    `
}

function addEventListener() {
    $('.delete-subtask').on('click', function () {
        $(this).parent().remove()
    })
}