// score

var comm_p = document.getElementById("commentary");

var comm_text;

if (score < 3) {
    comm_text = "Вам необходимо детально изучить все о кредитах!";
} else if (score < 6) {
    comm_text = "Ваши знания на среднем уровне.";
} else if (score < 9) {
    comm_text = "Ваши знания хороши, однако есть недочеты.";
} else {
    comm_text = "У вас отличные знания!";
}

comm_p.innerHTML = `${comm_text}`;