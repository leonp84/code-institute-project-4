$(function () {
    counter = 1
    $('#create-new-column').on('click', function () {
        counter ++
        $('#create-new-column').prev().append(extraCol(counter))
        $('.remove-button').on('click', function () {
            let y = `#remove-button-${
                counter - 1
            }`
            console.log(y)
            $(y).show()
            let x = `#col-${counter}`
            $(x).remove()
            if (counter != 1) {
                counter --
            }
        })
    })

    l_counter = 1
    $('#create-new-label').on('click', function () {
        l_counter ++
        $('#create-new-label').prev().append(extraLabel(l_counter))
        $('.remove-button-label').on('click', function () {
            let y = `#remove-button-label-${
                l_counter - 1
            }`
            console.log(y)
            $(y).show()
            let x = `#label-${l_counter}`
            $(x).remove()
            if (l_counter != 1) {
                l_counter --
            }
        })
    })
})


function extraCol(num) {
    $('.remove-button').hide()
    return `<div id="col-${num}">
    <hr>
    <div class="mb-3" >
    <label for="column_title" class="form-label requiredField">
        Column ${num} Title
        <span class="asteriskField">*</span>
    </label>
    <button type="button" class="btn-close mb-1 remove-button" aria-label="Close" id="remove-button-${num}"></button>
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
    $('.remove-button-label').hide()
    return `<div id="label-${num}">
        <hr>
        <div class="mb-3" >
        <label for="label_title" class="form-label requiredField">
            Label ${num} Title
            <span class="asteriskField">*</span>
        </label>
        <button type="button" class="btn-close mb-1 remove-button-label" aria-label="Close" id="remove-button-label-${num}"></button>
        <input type="text" name="label_title" maxlength="200" class="textinput form-control" required id="id_title-${num}">
        </div>
        <span class="mb-2">Choose a colour for Label ${num}:</span>
        <div class="mb-3">
        <input type="radio" class="btn-check" name="label_colour-${num}" value="0" id="black-${num}" checked>
        <label class="btn btn-outline-secondary" for="black-${num}">Black</label>
    
        <input type="radio" class="btn-check" name="label_colour-${num}" value="1" id="blue-${num}" >
        <label class="btn btn-outline-primary" for="blue-${num}">Blue</label>
    
        <input type="radio" class="btn-check" name="label_colour-${num}" value="2" id="green-${num}" >
        <label class="btn btn-outline-success" for="green-${num}">Green</label>
    
        </div>
        </div>`
}
