console.log(character)

var option = document.getElementsByName("product_name")[0];
var choice = undefined;
var input_details = document.getElementById("input_details");
var button = document.getElementById("submit")

option.addEventListener("change", function() {
    choice = option.value;
    createInputDetails(choice);
}) 
createInputDetails("mainloan");

function createInputDetails(choice) {
    switch(choice) {
        case "mainloan":
            if (checkCharaInfoML()) {
                input_details.innerHTML = `
                    <div id="input_field">
                        <label for="duration"><p id="duration_label">Продолжительность кредита: </p></label>
                        <input type="range" min="12" max="84" step="12" id="slider" name="duration" required />
                        <div class="ticks">
                            <p>12</p>
                            <p>24</p>
                            <p>36</p>
                            <p>48</p>
                            <p>60</p>
                            <p>72</p>
                            <p>84</p>
                        </div>
                    </div>
                    <div id="input_field">
                        <label for="amnt"><p id="amnt_label">Сумма кредита</p></label>
                        <input type="range" min="30000" max="2000000" step="10000" id="slider" name="amnt" required />
                        <div class="ticks amnt_ticks">
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                        </div>
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
                    var ticks_div = document.getElementsByClassName("amnt_ticks");
                    ticks_div.innerHTML += `<p></p><p></p>`;
                } else {
                    slider_amnt.min = 50000;
                }
            }
            break;
        case "targetloan":
            if (checkCharaInfoTL()) {
                input_details.innerHTML = `
                    <div id="input_field">
                        <label for="duration"><p id="duration_label">Продолжительность кредита</p></label>
                        <input type="range" min="1" max="60" id="slider" name="duration" required />
                        <div class="ticks">
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                        </div>
                    </div>
                    <div id="input_field">
                        <label for="amnt"><p id="amnt_label">Сумма кредита</p></label>
                        <input type="range" min="0" max="1500000" step="500" class="restricted" id="slider" name="amnt" required />
                        <div class="ticks">
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                            <p></p>
                        </div>
                    </div>
                    <div id="input_field">
                        <label for="hfz">Акция "Хочу 0"?</label>
                        <select name="hfz" required>
                            <option value="y">Да</option>
                            <option value="n">Нет</option>
                        </select>
                    </div>
                `;
                var slider = document.getElementsByClassName("restricted")[0];
                slider.addEventListener("input", () => {
                    if (slider.value < 1500) {
                        slider.value = 1500;
                    } 
                });
                setUpdateLabel();
            }
            break;
    }
}

function setUpdateLabel() {
    var duration = document.getElementsByName("duration")[0];
    var duration_label = document.getElementById("duration_label");
    duration_label.innerText = `Продолжительность кредита: ${duration.value} мес.`;
    duration.oninput = null;
    duration.addEventListener("input", function() {
        duration_label.innerText = `Продолжительность кредита: ${duration.value} мес.`;
    })

    var amnt = document.getElementsByName("amnt")[0];
    var amnt_label = document.getElementById("amnt_label");
    amnt_label.innerText = `Сумма кредита: ${amnt.value}₽`;
    amnt.oninput = null;
    amnt.addEventListener("input", function() {
        amnt_label.innerText = `Сумма кредита: ${amnt.value}₽`;
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
        input_details.innerHTML += `
            <p>Внимание: Ваш возраст не соответствует требованиям</p>
        `;
        button.disabled = true;
        return false;
    }
    if (!(character.citizenship == "Россия" || character.citizenship == "РФ")) {
        input_details.innerHTML += `
            <p>Внимание: продукт доступен только гражданам РФ</p>
        `
        button.disabled = true;
    } 
    return true;
}