def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_book(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()


    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

def test_get_one_book_with_no_record(client):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == None

def test_get_all_books_when_two_exist(client, two_saved_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()


    # Assert
    assert response.status_code == 200
    assert response_body == [{
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    },
    {
        "id" : 2,
        "title" : "Mountain Book", 
        "description" : "i luv 2 climb rocks"
    }]

def test_create_a_book_when_none_exist(client):
    response = client.post("/books", json=({"title": "t1", "description": "d1"}))

    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {"id" : 1, "title" : "t1", "description" : "d1"}