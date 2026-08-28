import json
import os

from app.data import QnaStore
from scripts.create_qna import append_qna
from scripts.validate_qna import validate_qna_dir


def test_append_qna_writes_loader_understandable_item(tmp_path):
    path = append_qna(
        str(tmp_path / "qna"),
        "ver1",
        "Memes",
        20,
        text="New question",
        code="int x = 1;",
        answer_text="New answer",
    )
    assert path.endswith(os.path.join("qna", "ver1", "Memes", "20.json"))
    data = json.load(open(path, encoding="utf-8"))
    assert data["qnas"] == [
        {
            "question": "New question",
            "cquestion": "int x = 1;",
            "answer": "New answer",
        }
    ]
    qna = QnaStore(str(tmp_path / "qna")).random_question("ver1", "Memes", 20)
    assert qna["text"] == "New question"
    assert qna["code"] == "int x = 1;"
    assert qna["answer"]["text"] == "New answer"


def test_append_qna_creates_dirs_when_missing(tmp_path):
    path = append_qna(str(tmp_path / "qna"), "ver1", "New Cat", 10, text="Hi")
    assert os.path.isfile(path)
    assert QnaStore(str(tmp_path / "qna")).categories("ver1") == ["New Cat"]


def test_append_qna_appends_to_existing_list(tmp_path):
    base = tmp_path / "qna" / "ver1" / "Memes"
    base.mkdir(parents=True)
    path = base / "10.json"
    path.write_text('{ "qnas": [ { "question": "first" } ] }')
    append_qna(str(tmp_path / "qna"), "ver1", "Memes", 10, text="second")
    data = json.load(open(path, encoding="utf-8"))
    assert len(data["qnas"]) == 2


def test_append_qna_timestamp_writes_utc_iso(tmp_path):
    path = append_qna(str(tmp_path / "qna"), "ver1", "Memes", 10, text="x", timestamp=True)
    data = json.load(open(path, encoding="utf-8"))
    created = data["qnas"][0]["created"]
    assert created.endswith("+00:00")


def test_validate_qna_dir_reports_empty_qnas(tmp_path):
    base = tmp_path / "qna" / "ver1" / "Cat"
    base.mkdir(parents=True)
    (base / "10.json").write_text('{ "qnas": [] }')
    messages = []
    errors, warnings = validate_qna_dir(str(tmp_path / "qna"), messages.append)
    assert messages and any("empty" in m for m in messages)
    assert errors >= 1


def test_validate_qna_dir_reports_missing_image(tmp_path):
    base = tmp_path / "qna" / "ver1" / "Memes"
    base.mkdir(parents=True)
    (base / "10.json").write_text(
        '{ "qnas": [ { "question": "q", "qimage": "qna/ver1/img/ghost.png", "answer": "a" } ] }'
    )
    messages = []
    errors, warnings = validate_qna_dir(str(tmp_path / "qna"), messages.append)
    assert any("file missing" in m for m in messages)
    assert errors >= 1


def test_validate_qna_dir_flags_stray_nonjson(tmp_path):
    base = tmp_path / "qna" / "ver1" / "WAP"
    base.mkdir(parents=True)
    (base / "10.c").write_text("// code\n")
    messages = []
    errors, warnings = validate_qna_dir(str(tmp_path / "qna"), messages.append)
    assert any(".c" in m and "stray" in m for m in messages)
    assert errors >= 1


def test_validate_qna_dir_warns_on_legacy_only_answer_missing(tmp_path):
    base = tmp_path / "qna" / "ver1" / "Cat"
    base.mkdir(parents=True)
    (base / "10.json").write_text('{ "qnas": [ { "question": "q" } ] }')
    messages = []
    errors, warnings = validate_qna_dir(str(tmp_path / "qna"), messages.append)
    assert any("no answer" in m for m in messages)
    assert warnings >= 1
    assert errors == 0
