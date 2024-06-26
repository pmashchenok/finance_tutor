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
            input_details.innerHTML = `
                <div id="input_field">
                    <label for="duration">Продолжительность кредита</label>
                    <input type="text" name="duration" required />
                </div>
                <div id="input_field">
                    <label for="amnt">Сумма кредита</label>
                    <input type="text" name="amnt" required />
                </div>
                <div id="input_field">
                    <label for="hfz">Акция "Хочу 0"?</label>
                    <select name="hfz" required>
                        <option value="y">Да</option>
                        <option value="n">Нет</option>
                    </select>
                </div>
            `;
            duration = document.getElementsByName("duration")[0];
            amnt = document.getElementsByName("duration")[0];
            hfz = document.getElementsByName("hfz")[0];

            duration.unbind("change");
            duration.addEventListener("change", checkDurationML);

            amnt.unbind("change");
            amnt.addEventListener("change", checkAmntML);
            break;
        case "targetloan":
            input_details.innerHTML = `
                <div id="input_field">
                    <label for="duration">Продолжительность кредита</label>
                    <input type="text" name="duration" required />
                </div>
                <div id="input_field">
                    <label for="amnt">Сумма кредита</label>
                    <input type="text" name="amnt" required />
                </div>
                <div id="input_field">
                    <label for="hfz">Акция "Хочу 0"?</label>
                    <select name="hfz" required>
                        <option value="y">Да</option>
                        <option value="n">Нет</option>
                    </select>
                </div>
            `;
            duration = document.getElementsByName("duration")[0];
            amnt = document.getElementsByName("duration")[0];
            hfz = document.getElementsByName("hfz")[0];

            duration.unbind("change");
            duration.addEventListener("change", checkDurationML);

            amnt.unbind("change");
            amnt.addEventListener("change", checkAmntML);
 
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
