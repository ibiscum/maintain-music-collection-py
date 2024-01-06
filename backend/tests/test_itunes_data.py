import json
import pytest

from app.api import crud


# @pytest.mark.skip(reason="no way of currently testing this")
def test_create_track(test_app, monkeypatch):
    test_request_payload = {
        "persistent_id": "TESTTESTTESTTEST",
        "track_id": 100000,
        "track_name": "Test",
        "artist": "Test",
        "album_artist": "Test",
        "album": "Test",
        "genre": "Test",
        "disc_number": 1,
        "disc_count": 1,
        "track_number": 1,
        "track_count": 1,
        "album_year": "1970-01-01",
        "date_modified": "1970-01-01T00:00:00",
        "date_added": "1970-01-01T00:00:00",
        "volume_adjustment": 0,
        "play_count": 0,
        "play_date_utc": "1970-01-01T00:00:00",
        "artwork_count": 0,
        "md5_id": "ffff0000ffff0000ffff0000ffff0000"
    }

    test_response_payload = {
        "persistent_id": "TESTTESTTESTTEST",
        "track_id": 100000,
        "track_name": "Test",
        "artist": "Test",
        "album_artist": "Test",
        "album": "Test",
        "genre": "Test",
        "disc_number": 1,
        "disc_count": 1,
        "track_number": 1,
        "track_count": 1,
        "album_year": "1970-01-01",
        "date_modified": "1970-01-01T00:00:00",
        "date_added": "1970-01-01T00:00:00",
        "volume_adjustment": 0,
        "play_count": 0,
        "play_date_utc": "1970-01-01T00:00:00",
        "artwork_count": 0,
        "md5_id": "ffff0000ffff0000ffff0000ffff0000"
    }

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post(
        "/itunes_data/",
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


# @pytest.mark.skip(reason="no way of currently testing this")
def test_create_track_invalid_json(test_app):
    response = test_app.post(
        "/itunes_data/",
        content=json.dumps(
            {
                "persistent_id": "AAAATESTTESTTEST",
                "track_id": 100000,
                "track_name": "Test",
                "artist": "Test",
                "album_artist": "Test",
                "album": "Test",
                "genre": "Test",
                "disc_number": 1,
                "disc_count": 1,
                "track_number": 1,
                "track_count": 1
            }
        )
    )
    assert response.status_code == 422

    # response = test_app.post(
    #     "/itunes_data/",
    #     content=json.dumps(
    #         {
    #             "persistent_id": "BBBBTESTTESTTEST",
    #             "track_id": "100000",
    #             "track_name": "Test",
    #             "artist": "Test",
    #             "album_artist": "Test",
    #             "album": "Test",
    #             "genre": "Test",
    #             "disc_number": 1,
    #             "disc_count": 1,
    #             "track_number": 1,
    #             "track_count": 1,
    #             "album_year": "1970-01-01",
    #             "date_modified": "1970-01-01T00:00:00",
    #             "date_added": "1970-01-01T00:00:00",
    #             "volume_adjustment": 0,
    #             "play_count": 0,
    #             "play_date_utc": "1970-01-01T00:00:00",
    #             "artwork_count": 0,
    #             "md5_id": "ffff0000ffff0000ffff0000ffff0000"
    #         }
    #     )
    # )
    # assert response.status_code == 422


# @pytest.mark.skip(reason="no way of currently testing this")
def test_read_track(test_app, monkeypatch):
    test_data = {
        "persistent_id": "TESTTESTTESTTEST",
        "track_id": 100000,
        "track_name": "Test",
        "artist": "Test",
        "album_artist": "Test",
        "album": "Test",
        "genre": "Test",
        "disc_number": 1,
        "disc_count": 1,
        "track_number": 1,
        "track_count": 1,
        "album_year": "1970-01-01",
        "date_modified": "1970-01-01T00:00:00",
        "date_added": "1970-01-01T00:00:00",
        "volume_adjustment": 0,
        "play_count": 0,
        "play_date_utc": "1970-01-01T00:00:00",
        "artwork_count": 0,
        "md5_id": "ffff0000ffff0000ffff0000ffff0000"
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/itunes_data/TESTTESTTESTTEST")
    assert response.status_code == 200
    assert response.json() == test_data


# @pytest.mark.skip(reason="no way of currently testing this")
def test_read_track_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/itunes_data/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Entry not found"


@pytest.mark.skip(reason="no way of currently testing this")
def test_read_track_wrong_type_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/itunes_data/0")
    assert response.status_code == 422
    assert response.json()["detail"] == "Wrong type of ID"


# @pytest.mark.skip(reason="no way of currently testing this")
def test_read_all_tracks(test_app, monkeypatch):
    test_data = [
        {
            "persistent_id": "AAAATESTTESTTEST",
            "track_id": 100000,
            "track_name": "Test",
            "artist": "Test",
            "album_artist": "Test",
            "album": "Test",
            "genre": "Test",
            "disc_number": 1,
            "disc_count": 1,
            "track_number": 1,
            "track_count": 1,
            "album_year": "1970-01-01",
            "date_modified": "1970-01-01T00:00:00",
            "date_added": "1970-01-01T00:00:00",
            "volume_adjustment": 0,
            "play_count": 0,
            "play_date_utc": "1970-01-01T00:00:00",
            "artwork_count": 0,
            "md5_id": "ffff0000ffff0000ffff0000ffff0000"
        },
        {
            "persistent_id": "BBBBTESTTESTTEST",
            "track_id": 100001,
            "track_name": "Test",
            "artist": "Test",
            "album_artist": "Test",
            "album": "Test",
            "genre": "Test",
            "disc_number": 1,
            "disc_count": 1,
            "track_number": 1,
            "track_count": 1,
            "album_year": "1970-01-01",
            "date_modified": "1970-01-01T00:00:00",
            "date_added": "1970-01-01T00:00:00",
            "volume_adjustment": 0,
            "play_count": 0,
            "play_date_utc": "1970-01-01T00:00:00",
            "artwork_count": 0,
            "md5_id": "ffff0000ffff0000ffff0000ffff1111"
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/itunes_data/")
    assert response.status_code == 200
    assert response.json() == test_data


@pytest.mark.skip(reason="no way of currently testing this")
def test_update_track(test_app, monkeypatch):
    test_data = {
        "track_id": 100000,
        "track_name": "Test_Update",
        "artist": "Test_Update",
        "album_artist": "Test_Update",
        "album": "Test_Update",
        "genre": "Test_Update",
        "disc_number": 1,
        "disc_count": 1,
        "track_number": 1,
        "track_count": 1,
        "album_year": "1970-02-02",
        "date_modified": "1970-02-02T00:00:00",
        "date_added": "1970-02-02T00:00:00",
        "volume_adjustment": 0,
        "play_count": 0,
        "play_date_utc": "1970-02-02T00:00:00",
        "artwork_count": 0,
        "md5_id": "ffff0000ffff0000ffff0000ffffaaaa",
        "persistent_id": "TESTTESTTESTTEST"
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("TESTTESTTESTTEST",
                            content=json.dumps(test_data))
    assert response.status_code == 200
    assert response.json() == test_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        ["TESTTESTTESTTEST", {}, 422],
        # [1, {"description": "bar"}, 422],
        [
            "EEEETESTTESTTEST",
            {
                "track_id": 100000,
                "track_name": "Test_Update",
                "artist": "Test_Update",
                "album_artist": "Test_Update",
                "album": "Test_Update",
                "genre": "Test_Update",
                "disc_number": 1,
                "disc_count": 1,
                "track_number": 1,
                "track_count": 1,
                "album_year": "1970-02-02",
                "date_modified": "1970-02-02T00:00:00",
                "date_added": "1970-02-02T00:00:00",
                "volume_adjustment": 0,
                "play_count": 0,
                "play_date_utc": "1970-02-02T00:00:00",
                "artwork_count": 0,
                "md5_id": "ffff0000ffff0000ffff0000ffffaaaa"
            },
            404
        ],
    ],
)
# @pytest.mark.skip(reason="no way of currently testing this")
def test_update_track_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/itunes_data/{id}", content=json.dumps(payload),)
    assert response.status_code == status_code


# @pytest.mark.skip(reason="no way of currently testing this")
def test_remove_track(test_app, monkeypatch):
    test_data = {
        "persistent_id": "TESTTESTTESTTEST",
        "track_id": 100000,
        "track_name": "Test_Update",
        "artist": "Test_Update",
        "album_artist": "Test_Update",
        "album": "Test_Update",
        "genre": "Test_Update",
        "disc_number": 1,
        "disc_count": 1,
        "track_number": 1,
        "track_count": 1,
        "album_year": "1970-02-02",
        "date_modified": "1970-02-02T00:00:00",
        "date_added": "1970-02-02T00:00:00",
        "volume_adjustment": 0,
        "play_count": 0,
        "play_date_utc": "1970-02-02T00:00:00",
        "artwork_count": 0,
        "md5_id": "ffff0000ffff0000ffff0000ffffaaaa"
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/itunes_data/TESTTESTTESTTEST")
    assert response.status_code == 200
    assert response.json() == test_data


# @pytest.mark.skip(reason="no way of currently testing this")
def test_remove_track_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/itunes_data/AAAABBBBCCCCDDDD")
    assert response.status_code == 404
    assert response.json()["detail"] == "Entry not found"
