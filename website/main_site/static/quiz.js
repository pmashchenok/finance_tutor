// test: list of questions
// question: index + text + labels
// results_url: link to results page

var steps = 0;
var nQuestions = test.length;
var div = document.getElementsByClassName("question_container")[0];
var answers = [];

function getQuestion() {
    steps += 1;
    const question = test[steps-1];
    if (steps < nQuestions) {
        div.innerHTML = `
            <h2>№${steps}. ${question.text}</h2>
            <div class="questions">
                <label class="question">
                    <input type="radio" name="question" value="1" />
                    <span>${question.labels[0]}</span> 
                </label>
                <label class="question"> 
                    <input type="radio" name="question" value="2" />
                    <span>${question.labels[1]}</span>
                </label>
                <label class="question"> 
                    <input type="radio" name="question" value="3" />
                    <span>${question.labels[2]}</span>
                </label>
                <label class="question"> 
                    <input type="radio" name="question" value="4" />
                    <span>${question.labels[3]}</span>
                </label>
            </div>
            <button class="submit_button" type="button" onclick="getAnswer();">→</button>
        `;
    } else {
         div.innerHTML = `
            <h2>№${steps}. ${question.text}</h2>
            <div class="questions">
                <label class="question">
                    <input type="radio" name="question" value="1" />
                    <span>${question.labels[0]}</span> 
                </label>
                <label class="question"> 
                    <input type="radio" name="question" value="2" />
                    <span>${question.labels[1]}</span>
                </label>
                <label class="question"> 
                    <input type="radio" name="question" value="3" />
                    <span>${question.labels[2]}</span>
                </label>
                <label class="question"> 
                    <input type="radio" name="question" value="4" />
                    <span>${question.labels[3]}</span>
                </label>
            </div>
            <form action="${results_url}" method="GET" name="form">
                <button class="submit_button" type="submit" name="results" onclick="getAnswer();" value="">Завершить тест</button>
            </form> 
        `;
    }

}

function next() {
    if (steps < nQuestions) {
        getQuestion();
    } else {
        document.form.results.value = answers;
    }
}

function getAnswer() {
    const selectedAnswer = document.querySelector("input[name='question']:checked").value;
    answers.push(selectedAnswer);
    next();
}

getQuestion();