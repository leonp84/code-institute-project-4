$(function () {

    colCounter = 2


    $('#create-new-column').on('click', function () {
        $('#create-new-column').prev().append(extraCol(colCounter))
        $('#remove-new-column').show()
        colCounter ++
    })

    $('#remove-new-column').on('click', function () {
        let latest_col = `#col-${colCounter-1}`
        $(latest_col).remove()
        if (colCounter != 1) {
            colCounter --
        }
        if (colCounter == 2) {
            $('#remove-new-column').hide()
        }
    })

    labelCounter = 2

    $('#create-new-label').on('click', function () {
        $('#create-new-label').prev().append(extraLabel(labelCounter))
        $('#remove-new-label').show()
        labelCounter ++
    })

    $('#remove-new-label').on('click', function () {
        let latest_label = `#label-${labelCounter-1}`
        $(latest_label).remove()
        if (labelCounter != 1) {
            labelCounter --
        }
        if (labelCounter == 2) {
            $('#remove-new-label').hide()
        }
    })
})


function extraCol(num) {
    return `
    
    <div id="col-${num}">
        <hr>
        <div class="mb-3" >
            <label for="column_title" class="form-label requiredField">
                Column ${num} Title
                <span class="asteriskField">*</span>
            </label>
            <input type="text" name="column_title" maxlength="200" class="textinput form-control" required id="id_title-${num}">
        </div>

        <span class="mb-2">Choose a colour for Column ${num}:</span>

        <div class="mb-3">
            <input type="radio" class="btn-check" name="column_colour-${num}" value="0" id="black-${num}" checked>
            <label class="btn btn-outline-secondary" for="black-${num}">Black</label>

            <input type="radio" class="btn-check" name="column_colour-${num}" value="1" id="blue-${num}" >
            <label class="btn btn-outline-primary" for="blue-${num}">Blue</label>

            <input type="radio" class="btn-check" name="column_colour-${num}" value="2" id="green-${num}" >
            <label class="btn btn-outline-success" for="green-${num}">Green</label>
        </div>
    </div>`
}


function extraLabel(num) {
    return `
    
    <div id="label-${num}">
        <hr>
        <div class="mb-3">
            <label for="label_title" class="form-label requiredField">
                Label ${num} Title
                <span class="asteriskField">*</span>
            </label>
            <button type="button" class="btn-close mb-1 remove-button-label" aria-label="Close"
                id="remove-button-label-${num}"></button>
            <input type="text" name="label_title" maxlength="200" class="textinput form-control" required
                id="id_title-${num}">
        </div>
        <span class="mb-2">Choose a colour for Label ${num}:</span>
        <div class="mb-3">
            <input type="radio" class="btn-check" name="label_colour-${num}" value="0" id="black-${num}" checked>
            <label class="btn btn-outline-secondary" for="black-${num}">Black</label>

            <input type="radio" class="btn-check" name="label_colour-${num}" value="1" id="blue-${num}">
            <label class="btn btn-outline-primary" for="blue-${num}">Blue</label>

            <input type="radio" class="btn-check" name="label_colour-${num}" value="2" id="green-${num}">
            <label class="btn btn-outline-success" for="green-${num}">Green</label>

        </div>
    </div>`
}
