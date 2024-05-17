$(function () {

    // Find number of last current column on board
    let colCounter = parseInt($('.column-counter').last().text()) + 1;
    let startColCounter = colCounter;

    // Populate new Column on Edit Board Page
    $('#create-new-column').on('click', function () {
        $('#create-new-column').prev().append(extraCol(colCounter));
        $('#remove-new-column').show();
        checkColumnNameDuplicates();
        colCounter++;
    });

    // Remove newly populated Column on Edit Board Page
    $('#remove-new-column').on('click', function () {
        let latest_col = `#col-${colCounter - 1}`;
        $(latest_col).remove();
        colCounter--;
        // Users cannot remove existing Columns
        if (colCounter == startColCounter) {
            $('#remove-new-column').hide();
        }
    });

    // Find number of last current label on board
    let labelCounter = parseInt($('.label-counter').last().text()) + 1;
    let startLabelCounter = labelCounter;

    // Populate new Label on Edit Board Page
    $('#create-new-label').on('click', function () {
        $('#create-new-label').prev().append(extraLabel(labelCounter));
        $('#remove-new-label').show();
        labelCounter++;
    });

    // Remove newly populated Label on Edit Board Page
    $('#remove-new-label').on('click', function () {
        let latest_label = `#label-${labelCounter - 1}`;
        $(latest_label).remove();
        labelCounter--;
        // Users cannot remove existing Labels
        if (labelCounter == startLabelCounter) {
            $('#remove-new-label').hide();
        }
    });

    // Add Event Listeners to check for title duplicates
    checkBoardNameDuplicates();
    checkColumnNameDuplicates();

});

function checkBoardNameDuplicates() {
    /**
     * Block users from entering duplicate board names
     */

    // Retrieve list of current board names
    let currentBoards = [];
    let saved_boards = document.getElementsByClassName('board-name');
    for (let i = 0; i < saved_boards.length; i++) {
        currentBoards.push(saved_boards[i].innerText);
    }

    // Remove name of current board from list (to allow resaving with same name)
    let current_name = document.getElementById('id_title').value;
    let index = currentBoards.indexOf(current_name);
    currentBoards.splice(index, 1);

    let errorState = false;
    document.getElementById('id_title').addEventListener('keydown', function (e) {

        // Handle Backspace character
        let user_input = this.value + e.key;
        if (e.key == 'Backspace') {
            user_input = this.value.slice(0, -1);
        }

        if (currentBoards.includes(user_input)) {
            $('#id_title').css('border', '1px solid red');
            $('#id_title').prev().text('A Board with that name already exists');
            $('#id_title').prev().css('color', 'red');
            $('#edit-current-board').addClass('disabled');
            errorState = true;
        } else {
            if (errorState) {
                $('#id_title').css('border', '1px solid #dee2e6');
                $('#id_title').prev().text('Title *');
                $('#id_title').prev().css('color', '#383140');
                $('#edit-current-board').removeClass('disabled');
                errorState = false;
            }
        }
    });
}

function checkColumnNameDuplicates() {
    /**
     * Block users from entering duplicate column names
     */
    let errorState = false;

    $('input[name="column_title"]').on('keydown', function (e) {

        // Handle Backspace character
        let currentInput = this.value + e.key;
        if (e.key == 'Backspace') {
            currentInput = this.value.slice(0, -1);
        }

        // Get current column names from unfocused input fields
        let currentCols = [];
        let allInputs = $('.col-titles');
        let unfocusedInputs = allInputs.not(':focus');
        for (let i = 0; i < unfocusedInputs.length; i++) {
            currentCols.push(unfocusedInputs[i].value);
        }

        // Check if currently inputted column name is a duplicate
        if (currentCols.includes(currentInput)) {
            $(this).css('border', '1px solid red');
            $(this).prev().text('Duplicate Column Names Are Not Recommended');
            $(this).prev().css('color', 'red');
            $('#edit-current-board').addClass('disabled');
            errorState = true;
        } else {
            if (errorState) {
                $(this).css('border', '1px solid #dee2e6');
                $(this).prev().text('Title *');
                $(this).prev().css('color', '#383140');
                $('#edit-current-board').removeClass('disabled');
                errorState = false;
            }
        }
    });
}

function extraCol(num) {
    /**
     * Populate extra column input with custom HTML
     */
    return `
    <div id="col-${num}">
        <hr>
        <div class="mb-3">
            <label for="id_title-${num}" class="form-label requiredField">
                Column ${num} Title
                <span class="asteriskField">*</span>
            </label>
            <input type="text" name="column_title" maxlength="200" class="textinput form-control col-titles" pattern="[^\s].*" required id="id_title-${num}">
        </div>
        <span class="mb-2">Choose a colour for Column ${num}:</span>
        <div class="mb-3">
            <input type="radio" class="btn-check" name="column_colour-${num}" value="white" id="white-${num}" checked>
            <label class="btn btn btn-light colour-selector" for="white-${num}">White</label>
            <input type="radio" class="btn-check" name="column_colour-${num}" value="red" id="red-${num}">
            <label class="btn btn-outline-danger colour-selector" for="red-${num}">Red</label>
            <input type="radio" class="btn-check" name="column_colour-${num}" value="green" id="green-${num}">
            <label class="btn btn-outline-success colour-selector" for="green-${num}">Green</label>
            <input type="radio" class="btn-check" name="column_colour-${num}" value="blue" id="blue-${num}">
            <label class="btn btn-outline-primary colour-selector" for="blue-${num}">Blue</label>
            <input type="radio" class="btn-check" name="column_colour-${num}" value="yellow" id="yellow-${num}">
            <label class="btn btn-outline-warning colour-selector" for="yellow-${num}">Yellow</label>
        </div>
    </div>`;
}

function extraLabel(num) {
    /**
     * Populate extra label form with custom HTML
     */
    return `
    <div id="label-${num}">
        <hr>
        <div class="mb-3">
            <label for="label_title-${num}" class="form-label requiredField">
                Label ${num} Title
                <span class="asteriskField">*</span>
            </label>
            <button type="button" class="btn-close mb-1 remove-button-label" aria-label="Close" id="remove-button-label-${num}"></button>
            <input type="text" name="label_title" maxlength="200" class="textinput form-control" required id="label_title-${num}">
        </div>
        <span class="mb-2">Choose a colour for Label ${num}:</span>
        <div class="mb-3">
            <input type="radio" class="btn-check" name="label_colour-${num}" value="light" id="label-white-${num}" checked>
            <label class="btn btn btn-light colour-selector" for="label-white-${num}">White</label>
            <input type="radio" class="btn-check" name="label_colour-${num}" value="danger" id="label-red-${num}">
            <label class="btn btn-outline-danger colour-selector" for="label-red-${num}">Red</label>
            <input type="radio" class="btn-check" name="label_colour-${num}" value="success" id="label-green-${num}">
            <label class="btn btn-outline-success colour-selector" for="label-green-${num}">Green</label>
            <input type="radio" class="btn-check" name="label_colour-${num}" value="primary" id="label-blue-${num}">
            <label class="btn btn-outline-primary colour-selector" for="label-blue-${num}">Blue</label>
            <input type="radio" class="btn-check" name="label_colour-${num}" value="warning" id="label-yellow-${num}">
            <label class="btn btn-outline-warning colour-selector" for="label-yellow-${num}">Yellow</label>
        </div>
    </div>`;
}