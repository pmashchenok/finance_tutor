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
var help_div = document.getElementsByClassName("help")[0];

info_div.innerHTML = `
    <h2>Информация</h2>
    <p>Баланс: <br><span id="stat">${char.balance}</span></p>
    <p>Сумма задолженности: <br><span id="stat">${state.debt}</span></p>
    <p>Месяц: <br><span id="stat">${state.turn}/${product.duration}</span></p>
`;

game_text_div.innerHTML = `
    <h2>${cur_event.character}</h2>
    <p>${cur_event.text}</p>
`;

if (cur_event.type == "CHOICE") {
    var inp = Object.entries(cur_event.inputs)[0];
    inputs_div.innerHTML = `
        <button name="game_input" class="choice_btn" type="submit" value="${inp[1]}">${inp[0]}</button>
    `;
} else if (cur_event.type == "INPUT") {
    var inps = cur_event.inputs;
    for (var propt in inps) {
        inputs_div.innerHTML += `
            <button name="game_input" class="input_btn" type="submit" value="${inps[propt]}">${propt}</button>
        `;
    }
} else if (cur_event.type == "CREDIT") {
    var inp = Object.entries(cur_event.inputs)[0];
    inputs_div.innerHTML = `
        <label for="game_input">${inp[0]}<br><input name="game_input" type="number" min="${annuity}"></label>
        <button type="submit">Далее</button>
    `
} else {
    var inp = Object.entries(cur_event.inputs)[0];
    inputs_div.innerHTML = `
        <a href="${home_url}"><button name="game_input" class="choice_btn" type="button">${inp[0]}</button></a>
    `;
}

other_character.innerHTML = `
    <img src="${static_url}/${cur_event.character}.png">
`;

character.innerHTML = `
    <img src="${static_url}/character.png">
`;

function showHelp() {
    if (help_div.style.display === "none") {
        help_div.style.display = "block";
        var product_str = state.product_type == "LOAN_MAIN" ? "кредит на любые цели" : "кредит на покупку товара"
        help_div.innerHTML = `
            <h2>Справка</h2>
            <p>Ваш продукт: ${product_str} на сумму ${state.product.amnt}₽, 
            продолжительность ${state.product.duration} мес.<br>
        `

        if (state.product_type == "LOAN_MAIN") {
            help_div.innerHTML += `
                Процентная ставка первого периода кредита: ${state.product.year_interest_1st_period*100}% 
                (${state.product.first_period_dur} мес.), процентная ставка второго периода кредита: ${state.product.year_interest_2nd_period*100}%.<br>
                Текущая ставка: ${state.product.year_interest*100}%.<br>
            `
        } else {
            help_div.innerHTML += `
                Процентная ставка: ${state.product.year_interest*100}%.<br>
            `
        }

        help_div.innerHTML += `
            Ежемесячные платежи вычисляются по формуле: <br><img src="${ann_url}" id="formula">,
            где <img id="big" src="${a_url}"> — ежемесячный платеж, <img id="big" src="${p_url}"> — сумма кредита, <img id="small" src="${r_url}"> — 
            месячная ставка (годовая ставка, поделенная на 12), <img id="small" src="${n_url}"> — срок кредита в месяцах.<br>
            Таким образом, Ваш ежемесячный платеж составляет ${annuity}₽.</p>
        `;
    } else {
        help_div.innerHTML = ``;
        help_div.style.display = "none";
    }
}