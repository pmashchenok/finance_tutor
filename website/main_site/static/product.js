var option = document.getElementsByName("product_name")[0];
var choice = undefined;
var input_details = document.getElementById("input_details");

option.addEventListener("change", function() {
    choice = option.value;
    createInputDetails(choice);
}) 

function createInputDetails(choice) {
    switch(choice) {
        case "mainloan":
            console.log(choice);
            // TODO Границы в зависимости от возраста и тд
            input_details.innerHTML = `
                <div id="input_field">
                    <label for="duration">Продолжительность кредита</label>
                    <input type="range" min="12" max="84" id="slider" name="duration" required />
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
            break;
        case "targetloan":
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
            break;
        case "cc2y":
            input_details.innerHTML = `
                <p>TODO!!!</p>
            `;
            break;
        case "cc200d":
            input_details.innerHTML = `
                <p>TODO!!!</p>
            `;
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