let data = [];
let category = '';
let value = '';
let getFields = document.getElementsByClassName('cb');
for (let i = 0; i < getFields.length; i++) {
    getFields[i].addEventListener('click', cbClick.bind(this, getFields[i]));
}

function cbClick(btn) {
    btn.style.visibility = 'hidden';
    category = btn.value
    value = btn.innerText
    getQnA()
}

function show() {
    console.log(data);
    document.getElementById("question").innerHTML = data['question'];
    document.getElementById("answer").innerHTML = data['answer'];
}

function getQnA() {
    let bodyData = JSON.stringify({
        'version': '1',
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