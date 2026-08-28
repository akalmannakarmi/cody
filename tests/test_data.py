import os
import random

from app.data import QnaStore


def test_versions_lists_subdirs(store):
    assert store.versions() == ["all", "ver1"]


def test_categories_excludes_img_and_hidden(tmp_path):
    base = tmp_path / "qna" / "ver1"
    (base / "Hist").mkdir(parents=True)
    (base / "img").mkdir()
    (base / ".hidden").mkdir()
    store = QnaStore(str(tmp_path / "qna"))
    assert store.categories("ver1") == ["Hist"]


def test_values_are_sorted_ints(store):
    assert store.values("ver1", "Memes") == [10, 20, 50]


def test_value_ignores_non_integer_files(tmp_path):
    base = tmp_path / "qna" / "ver1" / "Memes"
    base.mkdir(parents=True)
    (base / "abc.json").write_text("{}")
    (base / "9999.json").write_text("{}")
    store = QnaStore(str(tmp_path / "qna"))
    assert store.values("ver1", "Memes") == []


def test_normalization_mapping(store):
    qna = store.random_question("ver1", "Memes", 10)
    assert qna["text"] == "Fixture question one"
    assert qna["code"] is None
    assert qna["image"] is None
    assert qna["answer"] == {
        "text": "Fixture answer one",
        "code": None,
        "image": None,
    }


def test_normalization_image_url(store):
    qna = store.random_question("ver1", "Memes", 50)
    assert qna["text"] is None
    assert qna["code"] is None
    assert qna["image"] == "/getImg/qna/ver1/img/pic.png"
    assert qna["answer"]["text"] == "Image answer"


def test_random_question_missing_file(store):
    assert store.random_question("ver1", "Memes", 999) is None


def test_random_question_empty_qnas(store):
    assert store.random_question("ver1", "Extra", 10) is None


def test_normalization_code_keys(tmp_path):
    base = tmp_path / "qna" / "v" / "Cat"
    base.mkdir(parents=True)
    (base / "10.json").write_text(
        '{ "qnas": [ { "cquestion": "int x = 1;", "canswer": "int y = 2;" } ] }'
    )
    store = QnaStore(str(tmp_path / "qna"))
    qna = store.random_question("v", "Cat", 10)
    assert qna["code"] == "int x = 1;"
    assert qna["answer"]["code"] == "int y = 2;"


def test_random_question_uses_seeded_rng(tmp_path):
    base = tmp_path / "qna" / "v" / "Cat"
    base.mkdir(parents=True)
    (base / "10.json").write_text(
        '{ "qnas": [ {"question": "A"}, {"question": "B"}, {"question": "C"} ] }'
    )
    rng = random.Random(42)
    store = QnaStore(str(tmp_path / "qna"), rng=rng)
    seen = {store.random_question("v", "Cat", 10)["text"] for _ in range(10)}
    assert seen == {"A", "B", "C"}


def test_mtime_cache_invalidation(tmp_path):
    base = tmp_path / "qna" / "v" / "Cat"
    base.mkdir(parents=True)
    path = base / "10.json"
    path.write_text('{ "qnas": [ {"question": "first"} ] }')
    store = QnaStore(str(tmp_path / "qna"))
    assert store.random_question("v", "Cat", 10)["text"] == "first"

    path.write_text('{ "qnas": [ {"question": "second"} ] }')
    assert store.random_question("v", "Cat", 10)["text"] == "second"


def test_mtime_cache_hits_same_mtime(tmp_path):
    base = tmp_path / "qna" / "v" / "Cat"
    base.mkdir(parents=True)
    path = base / "10.json"
    path.write_text('{ "qnas": [ {"question": "one"} ] }')
    store = QnaStore(str(tmp_path / "qna"))
    assert store.random_question("v", "Cat", 10)["text"] == "one"
    path.write_text('{ "qnas": [ {"question": "two"} ] }')
    qna = store.random_question("v", "Cat", 10)
    assert qna["text"] in ("one", "two")
