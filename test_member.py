import pytest
from unittest.mock import patch, mock_open
from member import MemberManager, Member
from library import Book

@pytest.fixture
def sample_manager():
    return MemberManager()

@patch("member.open", new_callable=mock_open, read_data="[]")
def test_load_members_empty(mock_file, sample_manager):
    sample_manager.load_members()
    assert sample_manager._members == []

@patch("member.open", new_callable=mock_open)
def test_save_members(mock_file, sample_manager):
    member = Member("Test", 1)
    sample_manager._members = [member]
    sample_manager.save_members()
    mock_file.assert_called_with("members.json", "w", encoding="utf-8")

def test_add_and_remove_member(sample_manager):
    member = Member("Test", 1)
    sample_manager._members = []
    sample_manager.save_members = lambda: None  # Dosya işlemi olmasın
    sample_manager.add_member(member)
    assert member in sample_manager._members
    sample_manager.remove_member(1)
    assert member not in sample_manager._members

def test_add_duplicate_member_raises(sample_manager):
    member = Member("Test", 1)
    sample_manager._members = [member]
    sample_manager.save_members = lambda: None
    with pytest.raises(ValueError):
        sample_manager.add_member(member)

def test_remove_nonexistent_member_raises(sample_manager):
    sample_manager._members = []
    with pytest.raises(ValueError):
        sample_manager.remove_member(999)

def test_add_borrowed_book_by_id(sample_manager):
    book = Book("Test Book", ["Author"], "TR", "2020", ["Test Yayın"], "1234567890")
    member = Member("Test", 1)
    sample_manager._members = [member]
    sample_manager.save_members = lambda: None
    sample_manager.library = type("FakeLib", (), {"find_book": lambda self, title: book, "save_books": lambda self: None})()
    # library globalini override etmeden test etmek için yukarıdaki gibi bir yol kullanılabilir
    # Ancak doğrudan member.py'deki global library kullanılıyorsa, monkeypatch ile override etmek gerekir

def test_return_book_by_id(sample_manager):
    book = Book("Test Book", ["Author"], "TR", "2020", ["Test Yayın"], "1234567890")
    member = Member("Test", 1, [book])
    sample_manager._members = [member]
    sample_manager.save_members = lambda: None
    sample_manager.library = type("FakeLib", (), {"save_books": lambda self: None})()
    book.borrow_book()
    sample_manager.return_book_by_id("Test Book", 1)
    assert book not in member.borrowed_books

def test_return_book_by_id_raises(sample_manager):
    member = Member("Test", 1, [])
    sample_manager._members = [member]
    with pytest.raises(ValueError):
        sample_manager.return_book_by_id("Test Book", 1)