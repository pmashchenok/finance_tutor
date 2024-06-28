// state: GameState from gamec.py
// game_url: url of the "game.html" page

var char = state.char;
var product = state.product;
var cur_event = state.event;

var other_character = document.getElementsByClassName("other_character")[0];
var character = document.getElementsByClassName("character")[0];
var game_text_div = document.getElementsByClassName("game_text")[0];
var inputs_div = document.getElementsByClassName("inputs")[0];
var info_div = document.getElementsByClassName("info")[0];

info_div.innerHTML = `
    <h6>Информация</h6>
    <p>Баланс: ${char.balance}</p>
    <p>Сумма задолженности: ${state.debt}</p>
    <p>Месяц: ${state.turn}/${product.duration}</p>
`

game_text_div.innerHTML = `
    <h6>${cur_event.character}</h6>
    <p>${cur_event.text}</p>
`

if (cur_event.type == "CHOICE") {
    var inp = Object.entries(cur_event.inputs)[0];
    inputs_div.innerHTML = `
        <button name="game_input" class="choice_btn" type="submit" value="${inp[1]}">${inp[0]}</button>
    `
} else {
    var inps = cur_event.inputs;
    for (var propt in inps) {
        inputs_div.innerHTML += `
            <button name="game_input" class="input_btn" type="submit" value="${inps[propt]}">${propt}</button>
        `
    }
}

other_character.innerHTML = `
    <img src="${cur_event.character}.png">
`

character.innerHTML = `
    <img src="character.png">
`