(function () {
    "use strict";

    var board = window.BOARD;
    if (!board) return;

    var boardEl = document.getElementById("board");
    if (!boardEl) return;

    var questionModal = new bootstrap.Modal(document.getElementById("modal-question"));
    var answerModal = new bootstrap.Modal(document.getElementById("modal-answer"));

    var categories = board.categories || [];
    var values = board.values || [];
    var version = board.version;

    buildBoard();

    var resetBtn = document.getElementById("reset-btn");
    if (resetBtn) {
        resetBtn.addEventListener("click", function () {
            var tiles = boardEl.querySelectorAll("button.tile");
            for (var i = 0; i < tiles.length; i++) {
                tiles[i].disabled = false;
                tiles[i].classList.remove("used");
            }
        });
    }

    var answerBtn = document.getElementById("answer-btn");
    if (answerBtn) {
        answerBtn.addEventListener("click", function () {
            questionModal.hide();
            setTimeout(function () {
                answerModal.show();
            }, 300);
        });
    }

    function buildBoard() {
        boardEl.innerHTML = "";

        var headerRow = document.createElement("div");
        headerRow.className = "row mb-1";
        for (var c = 0; c < categories.length; c++) {
            var col = document.createElement("div");
            col.className = "col text-center";
            var hdr = document.createElement("p");
            hdr.className = "fw-bold fs-5 text-warning mb-0";
            hdr.textContent = categories[c];
            col.appendChild(hdr);
            headerRow.appendChild(col);
        }
        boardEl.appendChild(headerRow);

        for (var v = 0; v < values.length; v++) {
            var row = document.createElement("div");
            row.className = "row mb-1";
            for (var c2 = 0; c2 < categories.length; c2++) {
                var col2 = document.createElement("div");
                col2.className = "col px-1";
                var tile = document.createElement("button");
                tile.className = "btn btn-secondary btn-lg w-100 tile";
                tile.textContent = values[v];
                tile.dataset.category = categories[c2];
                tile.dataset.value = values[v];
                tile.addEventListener("click", onTileClick);
                col2.appendChild(tile);
                row.appendChild(col2);
            }
            boardEl.appendChild(row);
        }
    }

    function onTileClick(e) {
        var tile = e.currentTarget;
        var cat = tile.dataset.category;
        var val = tile.dataset.value;

        tile.disabled = true;
        tile.classList.add("used");

        fetch("/qna", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ version: version, category: cat, value: val })
        })
            .then(function (resp) {
                return resp.json();
            })
            .then(function (data) {
                if (data.error) {
                    showModal("Question", data.error, null);
                    questionModal.show();
                    return;
                }
                var title = cat + " &mdash; " + val;
                document.getElementById("label-question").innerHTML = title;
                document.getElementById("label-answer").innerHTML = "Answer &mdash; " + cat + " / " + val;

                populateContent(data.question, "question");
                populateContent(data.answer, "answer");

                questionModal.show();
            })
            .catch(function () {
                showModal("Question", "Failed to load question.", null);
                questionModal.show();
            });
    }

    function populateContent(obj, prefix) {
        var textEl = document.getElementById(prefix + "-text");
        var codeEl = document.getElementById(prefix + "-code");
        var imgWrap = document.getElementById(prefix + "-img-wrap");
        var imgEl = document.getElementById(prefix + "-img");

        if (obj.text) {
            textEl.textContent = obj.text;
            textEl.classList.remove("d-none");
        } else {
            textEl.textContent = "";
            textEl.classList.add("d-none");
        }

        if (obj.code) {
            codeEl.textContent = obj.code;
            codeEl.classList.remove("d-none");
        } else {
            codeEl.textContent = "";
            codeEl.classList.add("d-none");
        }

        if (obj.image) {
            imgEl.src = obj.image;
            imgWrap.classList.remove("d-none");
        } else {
            imgEl.src = "";
            imgWrap.classList.add("d-none");
        }
    }

    function showModal(title, text) {
        document.getElementById("label-question").innerHTML = title;
        var textEl = document.getElementById("question-text");
        textEl.textContent = text;
        textEl.classList.remove("d-none");
        document.getElementById("question-code").classList.add("d-none");
        document.getElementById("question-img-wrap").classList.add("d-none");
    }
})();
