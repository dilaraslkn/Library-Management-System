import pytest
from unittest.mock import patch, mock_open
from library import Library, Book

@pytest.fixture
def sample_library():
    # Her test için yeni bir Library nesnesi
    return Library("Test Library")

def test_add_and_find_book(sample_library):
    book = Book("Test Book", ["Author"], "TR", "2020", ["Test Yayın"], "1234567890")
    sample_library._books = []  # Dosya işlemi olmadan başlat
    sample_library.add_book = lambda b: sample_library._books.append(b)
    sample_library.add_book(book)
    found = sample_library.find_book("Test Book")
    assert found.title == "Test Book"
    assert found.isbn == "1234567890"

@patch("library.open", new_callable=mock_open, read_data="[]")
def test_load_books(mock_file, sample_library):
    # load_books fonksiyonunu test et, dosya açma işlemi mock'lanır
    sample_library.load_books()
    mock_file.assert_called_with("library.json", "r", encoding="utf-8")

@patch("library.open", new_callable=mock_open)
def test_save_books(mock_file, sample_library):
    book = Book("Test Book", ["Author"], "TR", "2020", ["Test Yayın"], "1234567890")
    sample_library._books = [book]
    sample_library.save_books()
    mock_file.assert_called_with("library.json", "w", encoding="utf-8")

def test_remove_book(sample_library):
    book = Book("Test Book", ["Author"], "TR", "2020", ["Test Yayın"], "1234567890")
    sample_library._books = [book]
    sample_library.save_books = lambda: None  # Dosya işlemi olmasın
    sample_library.remove_book("1234567890")
    assert len(sample_library._books) == 0

def test_borrow_and_return_book():
    book = Book("Test Book", ["Author"], "TR", "2020", ["Test Yayın"], "1234567890")
    book.borrow_book()
    assert book.is_borrowed is True
    book.return_book()
    assert book.is_borrowed is False

def test_borrow_already_borrowed_book_raises():
    book = Book("Test Book", ["Author"], "TR", "2020", ["Test Yayın"], "1234567890")
    book.borrow_book()
    with pytest.raises(ValueError):
        book.borrow_book()

def test_return_not_borrowed_book_raises():
    book = Book("Test Book", ["Author"], "TR", "2020", ["Test Yayın"], "1234567890")
    with pytest.raises(ValueError):
        book.return_book()