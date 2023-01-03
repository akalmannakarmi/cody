let data = [];
let category = '';
let value = '';
let getFields = document.getElementsByClassName('cb');
for (let i = 0; i < getFields.length; i++) {
    getFields[i].addEventListener('click', cbClick.bind(this, getFields[i]));
}

function cbClick(btn) {
    btn.style.visibility = 'hidden';
    category = document.getElementById(btn.value).innerText
    value = btn.innerHTML
    getQnA()
}

function show() {
    console.log(data);
    document.getElementById("question").innerHTML = data['question'] ? data['question'] : "";
    document.getElementById("answer").innerHTML = data['answer'] ? data['answer'] : "";
    document.getElementById("question-code").innerHTML = data['cquestion'] ? data['cquestion'] : "";
    document.getElementById("answer-code").innerHTML = data['canswer'] ? data['canswer'] : "";

    document.getElementById("question-img").src = `${window.origin}/getImg/${data['qimage']}`;
    document.getElementById("answer-img").src = `${window.origin}/getImg/${data['aimage']}`;

    document.getElementById("question-img").style.visibility = data['qimage'] ? "visible" : "hidden";
    document.getElementById("answer-img").style.visibility = data['aimage'] ? "visible" : "hidden";

}

function getQnA() {
    let bodyData = JSON.stringify({
        'version': 'ver1',
        'category': category,
        'value': value
    })

    fetch(`${window.origin}/qna`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: bodyData
    }).then(response => response.json()).then(function(qna) {
        data = qna;
        show();
    });
}