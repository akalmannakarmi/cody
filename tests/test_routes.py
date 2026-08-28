import json


def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_versions_returns_200(client):
    response = client.get("/versions")
    assert response.status_code == 200
    assert len(response.data) > 0


def test_contact_returns_200(client):
    response = client.get("/contact")
    assert response.status_code == 200


def test_play_ver1_returns_200(client):
    response = client.get("/play?ver=ver1")
    assert response.status_code == 200


def test_play_all_returns_200(client):
    response = client.get("/play?ver=all")
    assert response.status_code == 200


def test_play_missing_ver_redirects(client):
    response = client.get("/play")
    assert response.status_code == 302
    assert "/play?ver=all" in response.headers["Location"]


def test_play_unknown_version_returns_404(client):
    response = client.get("/play?ver=does-not-exist")
    assert response.status_code == 404


def test_qna_happy_path(client):
    response = client.post(
        "/qna",
        data=json.dumps({"version": "ver1", "category": "Memes", "value": 10}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["category"] == "Memes"
    assert data["value"] == 10
    assert data["question"]["text"] == "Fixture question one"
    assert data["answer"]["text"] == "Fixture answer one"


def test_qna_missing_keys_returns_404(client):
    response = client.post(
        "/qna",
        data=json.dumps({"version": "ver1", "category": "Memes"}),
        content_type="application/json",
    )
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_qna_unknown_version_returns_404(client):
    response = client.post(
        "/qna",
        data=json.dumps({"version": "nope", "category": "Memes", "value": 10}),
        content_type="application/json",
    )
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_qna_unknown_category_returns_404(client):
    response = client.post(
        "/qna",
        data=json.dumps({"version": "ver1", "category": "Nope", "value": 10}),
        content_type="application/json",
    )
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_qna_unparseable_value_returns_404(client):
    response = client.post(
        "/qna",
        data=json.dumps({"version": "ver1", "category": "Memes", "value": "abc"}),
        content_type="application/json",
    )
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_qna_empty_file_returns_404(client):
    response = client.post(
        "/qna",
        data=json.dumps({"version": "ver1", "category": "Extra", "value": 10}),
        content_type="application/json",
    )
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_getimg_happy(client):
    response = client.get("/getImg/qna/ver1/img/pic.png")
    assert response.status_code == 200


def test_getimg_path_traversal(client):
    response = client.get("/getImg/../.git/config")
    assert response.status_code == 404


def test_getimg_directory_escape(client):
    response = client.get("/getImg/ver1/../../secret")
    assert response.status_code == 404


def test_getimg_non_image_extension(client):
    response = client.get("/getImg/qna/ver1/Memes/10.json")
    assert response.status_code == 404


def test_unknown_route_returns_404_html(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert "text/html" in response.content_type
