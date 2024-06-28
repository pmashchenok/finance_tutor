// state: GameState from gamec.py
// game_url: url of the "game.html" page

let char = state.char;
let product = state.product;
let cur_event = state.event;

let other_character = document.getElementsByClassName("other_character")[0];
let character = document.getElementsByClassName("character")[0];
let game_text_div = document.getElementsByClassName("game_text")[0];
let inputs_div = document.getElementsByClassName("inputs")[0];

game_text_div.innerHTML = `
    <h6>${cur_event.character}</h6>
    <p>${cur_event.text}</p>
`

if (cur_event.type == "CHOICE") {
    var inps = cur_event.inputs;
    for (var propt in inps) {
        inputs_div.innerHTML += `
            <button name="game_input" class="input_btn" type="submit" value="${inps[propt]}">${propt}</button>
        `
    }
} else {
    inputs_div.innerHTML = `
        <label for="input">${Object.keys(cur_event.inputs)[0]}</label>
        <input class="input_txt" type="number" name="game_input" />
        <button type="submit">ОК</button>
    `
}