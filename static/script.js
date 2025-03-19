let index = 0;

function startTest(tests) {
    showQuestion(tests);
}

function showQuestion(tests) {
    if (index >= tests.length) {
        document.getElementById("test-container").innerHTML = "Test tugadi";
        return;
    }
    
    let q = tests[index];
    let html = `<h3>${q.savol}</h3>`;
    
    q.variantlar.forEach((v, i) => {
        html += `<button onclick='checkAnswer(${i}, ${q.togri}, ${JSON.stringify(tests)})'>${v}</button>`;
    });

    document.getElementById("test-container").innerHTML = html;
}

function checkAnswer(selected, correct, tests) {
    let buttons = document.querySelectorAll("button");
    
    buttons[selected + 1].style.background = selected === correct ? "green" : "red";

    setTimeout(() => {
        index++;
        showQuestion(tests);
    }, 3000);
}
