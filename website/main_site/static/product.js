console.log(character)

var option = document.getElementsByName("product_name")[0];
var choice = undefined;
var input_details = document.getElementById("input_details");
var button = document.getElementById("submit")

if (!(character.citizenship == "Россия" || character.citizenship == "РФ")) {
    input_details.innerHTML = `
        <p>Внимание: продукт доступен только гражданам РФ</p>
    `
    button.disabled = true;
} 

option.addEventListener("change", function() {
    choice = option.value;
    createInputDetails(choice);
}) 

function createInputDetails(choice) {
    switch(choice) {
        case "mainloan":
            if (checkCharaInfoML()) {
                input_details.innerHTML = `
                    <div id="input_field">
                        <label for="duration">Продолжительность кредита</label>
                        <input type="range" min="12" max="84" step="12" id="slider" name="duration" required />
                        <p id="duration_label"></p>
                    </div>
                    <div id="input_field">
                        <label for="amnt">Сумма кредита</label>
                        <input type="range" min="30000" max="2000000" id="slider" name="amnt" required />
                        <p id="amnt_label"></p>
                    </div>
                    <div id="input_field">
                        <label for="hfz">Акция "Хочу 0"?</label>
                        <select name="hfz" required>
                            <option value="y">Да</option>
                            <option value="n">Нет</option>
                        </select>
                    </div>
                `;
                setUpdateLabel();
                var slider_amnt = document.getElementsByName("amnt")[0];
                if (character.client) {
                    slider_amnt.min = 30000;
                } else {
                    slider_amnt.min = 50000;
                }
            }
            break;
        case "targetloan":
            if (checkCharaInfoTL()) {
                input_details.innerHTML = `
                <div id="input_field">
                        <label for="duration">Продолжительность кредита</label>
                        <input type="range" min="1" max="60" id="slider" name="duration" required />
                        <p id="duration_label"></p>
                    </div>
                    <div id="input_field">
                        <label for="amnt">Сумма кредита</label>
                        <input type="range" min="1500" max="1500000" id="slider" name="amnt" required />
                        <p id="amnt_label"></p>
                    </div>
                    <div id="input_field">
                        <label for="hfz">Акция "Хочу 0"?</label>
                        <select name="hfz" required>
                            <option value="y">Да</option>
                            <option value="n">Нет</option>
                        </select>
                    </div>
                `;
                setUpdateLabel();
            }
            break;
        case "cc2y":
            checkCharaInfoCC();
            break;
        case "cc200d":
            checkCharaInfoCC();
            break;
    }
}

function setUpdateLabel() {
    var duration = document.getElementsByName("duration")[0];
    var duration_label = document.getElementById("duration_label");
    duration_label.innerText = `${duration.value}`;
    duration.oninput = null;
    duration.addEventListener("input", function() {
        duration_label.innerText = `${duration.value}`;
    })

    var amnt = document.getElementsByName("amnt")[0];
    var amnt_label = document.getElementById("amnt_label");
    amnt_label.innerText = `${amnt.value}`;
    amnt.oninput = null;
    amnt.addEventListener("input", function() {
        amnt_label.innerText = `${amnt.value}`;
    })
}

function checkCharaInfoML() {
    if ((character.client && character.age < 20)
        || (!character.client && character.age < 24)
        || (character.age > 70)) {
        input_details.innerHTML = `
            <p>Внимание: Ваш возраст не соответствует требованиям</p>
        `;
        button.disabled = true;
        return false;
    }
    if (character.work_exp < 3) {
        input_details.innerHTML = `
            <p>Внимание: Ваш опыт работы не соответствует требованиям</p>
        `;
        button.disabled = true;
    }
    return true;
}

function checkCharaInfoTL() {
    if (character.age < 20 || character.age > 80) {
        input_details.innerHTML = `
            <p>Внимание: Ваш возраст не соответствует требованиям</p>
        `;
        button.disabled = true;
        return false;
    }
    return true;
}

function checkCharaInfoCC() {
    if (character.age < 20 || character.age > 70) {
        input_details.innerHTML = `
            <p>Внимание: Ваш возраст не соответствует требованиям</p>
        `;
        button.disabled = true;
        return false;
    }
    return true;
}
