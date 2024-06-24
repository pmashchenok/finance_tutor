// test: list of questions
// question: index + text
// results_url: link to results page

var steps = 0;
var nQuestions = test.length;
var div = document.getElementsByClassName("question")[0];
var answers = [];

function getQuestion() {
    steps += 1;
    const question = test[steps-1];
    div.innerHTML = `
        <h2>№${steps}. ${question.text}</h2>
        <div class="question_container">
            <form class="questions">
                <label><input type="radio" id="button1" name="question" value="1" />1</label>
                <label><input type="radio" id="button2" name="question" value="2" />2</label>
                <label><input type="radio" id="button3" name="question" value="3" />3</label>
                <label><input type="radio" id="button4" name="question" value="4" />4</label>
            </form>
            <button class="submit_button" type="button" onclick="getAnswer();">Следующий вопрос</button>
        </div>
    `;
}

function next() {
    if (steps < nQuestions) {
        getQuestion();
    } else {
        div.innerHTML = `
            <form action="${results_url}" method="GET" name="form">
                <button type="submit" name="results" value="">Перейти к результатам</button>
            </form> 
        `;
        document.form.results.value = answers;
    }
}

function getAnswer() {
    const selectedAnswer = document.querySelector("input[name='question']:checked").value;
    answers.push(selectedAnswer);
    next();
}

getQuestion();