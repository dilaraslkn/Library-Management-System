import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, mock_open

from api import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_files():
    # library.json ve members.json dosya işlemlerini mock'la
    with patch("library.open", mock_open(read_data="[]")), \
         patch("member.open", mock_open(read_data="[]")):
        yield

def test_list_books_empty():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_book(monkeypatch):
    # add_book_by_isbn fonksiyonunu mock'la, dosya işlemi olmasın
    def fake_add_book_by_isbn(self, isbn):
        return None
    monkeypatch.setattr("library.Library.add_book_by_isbn", fake_add_book_by_isbn)
    response = client.post("/books", params={"isbn": "1234567890"})
    assert response.status_code == 200
    assert "Kitap başarıyla eklendi" in response.json()["message"]

def test_delete_book(monkeypatch):
    def fake_remove_book(self, isbn):
        return None
    monkeypatch.setattr("library.Library.remove_book", fake_remove_book)
    response = client.delete("/books/1234567890")
    assert response.status_code == 200
    assert "Kitap başarıyla silindi" in response.json()["message"]

def test_add_member(monkeypatch):
    def fake_add_member(self, member):
        return None
    monkeypatch.setattr("member.MemberManager.add_member", fake_add_member)
    response = client.post("/members", params={"name": "Test", "member_id": 1})
    assert response.status_code == 200
    assert "Üye başarıyla eklendi" in response.json()["message"]

def test_delete_member(monkeypatch):
    def fake_remove_member(self, member_id):
        return None
    monkeypatch.setattr("member.MemberManager.remove_member", fake_remove_member)
    response = client.delete("/members/1")
    assert response.status_code == 200
    assert "Üye başarıyla silindi" in response.json()["message"]

def test_borrow_book(monkeypatch):
    def fake_borrow(self, title, member_id):
        return None
    monkeypatch.setattr("member.MemberManager.add_borrowed_book_by_id", fake_borrow)
    response = client.post("/members/1/borrow", params={"title": "Test Book"})
    assert response.status_code == 200
    assert "Kitap ödünç verildi" in response.json()["message"]

def test_return_book(monkeypatch):
    def fake_return(self, title, member_id):
        return None
    monkeypatch.setattr("member.MemberManager.return_book_by_id", fake_return)
    response = client.post("/members/1/return", params={"title": "Test Book"})
    assert response.status_code == 200
    assert "Kitap iade edildi" in response.json()["message"]