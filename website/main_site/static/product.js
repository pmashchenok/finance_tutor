var option = document.getElementById("input_product");
var choice = undefined;
var input_details = document.getElementById("input_details");

option.addEventListener("click", function() {
    choice = option.value;
    createInputDetails(choice);
}) 

function createInputDetails(choice) {
    switch(choice) {
        case "mainloan":
            input_details.innerHTML = `
                <p>TODO!!!</p>
            `
        case "targetloan":
            input_details.innerHTML = `
                <p>TODO!!!</p>
            `
        case "cc2y":
            input_details.innerHTML = `
                <p>TODO!!!</p>
            `
        case "cc200d":
            input_details.innerHTML = `
                <p>TODO!!!</p>
            `
    }
}