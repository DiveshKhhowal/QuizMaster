import csv
import io


def create_quiz(client, title="Test Quiz", difficulty="easy", category="General"):
    response = client.post("/api/quizzes", json={
        "title": title,
        "difficulty": difficulty,
        "category": category,
    })
    return response.get_json()["id"]


def add_question(client, quiz_id, correct_option="B"):
    return client.post(f"/api/quizzes/{quiz_id}/questions", json={
        "text": "What is 1 + 1?",
        "option_a": "1",
        "option_b": "2",
        "option_c": "3",
        "option_d": "4",
        "correct_option": correct_option,
    })
def add_true_false_question(client, quiz_id, correct_option="A"):
    return client.post(f"/api/quizzes/{quiz_id}/questions", json={
        "text": "The Earth revolves around the Sun.",
        "question_type": "true_false",
        "option_a": "True",
        "option_b": "False",
        "correct_option": correct_option,
    })


def test_list_quizzes_empty(client):
    response = client.get("/api/quizzes")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_quiz(client):
    response = client.post("/api/quizzes", json={"title": "Maths"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Maths"
    assert data["difficulty"] == "easy"


def test_create_quiz_empty_title(client):
    response = client.post("/api/quizzes", json={"title": "  "})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_quiz_wrong_difficulty(client):
    response = client.post("/api/quizzes", json={
        "title": "Maths",
        "difficulty": "impossible",
    })
    assert response.status_code == 400


def test_create_quiz_duplicate_title(client):
    response1 = client.post("/api/quizzes", json={"title": "Geography"})
    assert response1.status_code == 201

    response2 = client.post("/api/quizzes", json={"title": "Geography"})
    assert response2.status_code == 400
    assert response2.get_json()["error"] == "A quiz with this title already exists"


def test_create_quiz_duplicate_title_case_insensitive(client):
    response1 = client.post("/api/quizzes", json={"title": "Science"})
    assert response1.status_code == 201

    response2 = client.post("/api/quizzes", json={"title": "science"})
    assert response2.status_code == 400
    assert response2.get_json()["error"] == "A quiz with this title already exists"

    response3 = client.post("/api/quizzes", json={"title": "History"})
    assert response3.status_code == 201


def test_filter_quizzes_by_difficulty(client):
    create_quiz(client, "Easy One", "easy")
    create_quiz(client, "Hard One", "hard")
    response = client.get("/api/quizzes?difficulty=hard")
    quizzes = response.get_json()
    assert len(quizzes) == 1
    assert quizzes[0]["title"] == "Hard One"


def test_filter_quizzes_by_category(client):
    create_quiz(client, "Physics Quiz", "medium", "Science")
    create_quiz(client, "Chemistry Quiz", "easy", "Science")
    create_quiz(client, "World History", "medium", "History")

    response = client.get("/api/quizzes?category=Science")