import json
import httpx
from dataclasses import dataclass

class Book:

    def __init__(
            self, 
            title: str, 
            authors: list | None, 
            language: str | None, 
            publish_date: str | None, 
            publishers: list | None,  
            isbn: str
            ):
        
        self.title = title
        self.authors = authors
        self.language = language
        self.publish_date = publish_date
        self.publishers = publishers
        self.isbn = isbn
        self.is_borrowed = False   # Yani kitap rafta, kimse almadı.

    
    def __str__(self) -> str:
        return f"{self.title} by {self.authors} (ISBN: {self.isbn})"

  
    def borrow_book(self):    # Kitap ödünç verildi

        if not self.is_borrowed:      # kitap rafta değilse
            self.is_borrowed = True   # ödünç alınmıştır
        else:
            raise ValueError(f"'{self.title}' is already borrowed.")  # zaten ödünç alınmışsa

    def return_book(self):   # bu fonksiyonla da geri veriyorum

        if self.is_borrowed:          # kitap raftaysa
            self.is_borrowed = False  # kitap geri verilmiştir
        else:
            raise ValueError(f"'{self.title}' was not borrowed.")  # kitap zaten rafta
        



class EBook(Book):
    def __init__(
            self,
            title: str, 
            authors: list | None, 
            language: str | None, 
            publish_date: str | None, 
            publishers: list | None, 
            isbn: str, 
            file_format: str | None
            ):
        
        super().__init__(title, authors, language, publish_date, publishers, isbn)
        self.file_format = file_format

    def __str__(self) -> str:
        return f"{super().__str__()} and [Format: {self.file_format}]"




class AudioBook(Book):
    def __init__(
            self, 
            title: str, 
            authors: list | None, 
            language: str | None, 
            publish_date: str | None, 
            publishers: list | None,
            isbn: str, 
            duration: int | None
            ):
        
        super().__init__(title, authors, language, publish_date, publishers, isbn)
        self.duration = duration

    def __str__(self) -> str:
        return f"{super().__str__()} [Duration: {self.duration} mins]"
    
class BrailleBook(Book):

    def __init__(
            self, 
            title: str, 
            authors: list | None, 
            language: str | None, 
            publish_date: str | None, 
            publishers: list | None,
            isbn: str, 
            ages: str | None
            ):
        
        super().__init__(title, authors, language, publish_date, publishers, isbn)
        self.ages = ages

    def __str__(self) -> str:
        return f"{super().__str__()} [Ages: {self.ages}]"
    


ebook = EBook(
    "1984", 
    ["George Orwell"], 
    "Türkçe", 
    "1949", 
    ["Can Yayınları"],
    "9789750718533",
    "EPUB"
)

audio_book = AudioBook(
    "Becoming", 
    ["Michelle Obama"], 
    "English",
    "2018",
    ["Random House Audio"],
    "9781524763138",
    780
)

braille_book = BrailleBook(
    "Altın Böcek",
    ["Edgar Allan Poe"],
    "Türkçe",
    "2023",
    ["Can Sanat Yayınları"],
    "9789750762208",
    "12 yaş ve üzeri"
)

book = Book(
    "Zamana Karşı",
    ["Simon Kernick"],
    "Türkçe",
    "2020",
    ["Olimpos Yayınları"],
    "9786257135689"
)


# veri çekerken authors ve languages bilgileri key lerin içine koyulmuş bu key leri çözecek olan class
class OpenLibraryResolver:
    BASE_URL = "https://openlibrary.org"

    def __init__(self, session=None):
        self.session = session or httpx.Client()

    def resolve(self, key):
        try:
            resp = self.session.get(f"{self.BASE_URL}{key}.json")
            if resp.status_code == 200:
                return resp.json().get("name", key)
        except Exception:
            return "Bilinmeyen"
        return "Bilinmeyen"




class Library:
    
    def __init__(self, name: str):
        self.name = name
        self._books = []  


# Bu fonksiyon JSON dosyasından kitapları yükler

    def load_books(self):  

        # Dosyayı aç ve veriyi yükle
        with open("library.json", "r", encoding = "utf-8") as file: 
            data_list = json.load(file)
        
        common_keys = ("title", "authors", "language", "publish_date", "publishers", "isbn")

        # Kitap türüne göre JSON dosyasındaki veriyi self._books listesine ekleme
        for data in data_list:
            if "file_format" in data:
               self._books.append(EBook(**{k: data.get(k) for k in common_keys + ("file_format",)}))

            elif "duration" in data: 
               self._books.append(AudioBook(**{k: data.get(k) for k in common_keys + ("duration",)}))

            elif "ages" in data: 
               self._books.append(BrailleBook(**{k: data.get(k) for k in common_keys + ("ages",)}))
        
            else:
                self._books.append(Book(**{k: data.get(k) for k in common_keys}))


        


    def save_books(self):

        # self._books listesindeki her bir nesneyi sözlüğe dönüştürme
        data_list = [b.__dict__ for b in self._books]

        with open("library.json", "w", encoding="utf-8") as file:
            json.dump(data_list, file, ensure_ascii=False, indent=4)



    def list_books(self):

        with open("library.json", "r", encoding = "utf-8") as file:
            data_list = json.load(file)
            for data in data_list:
                print(f"Title: {data['title']} | Authors: {data['authors']} | ISBN 13: {data['isbn']}")


    # manuel olarak kitap bilgisi eklenerek kitap kaydetme
    def add_book(self, book: Book):
        
        self._books.append(book)
        # Kitap bilgilerinin kalıcı olarak saklanması için 
        self.save_books()

        if book in self._books:
            raise ValueError("Eklemeye çalıştığınız kitap zaten mevcut!")

        


    # API ile veri çekerek isbn numarasına göre kitap bilgilerini alma ve kaydetme
    def add_book_by_isbn(self, isbn: str):

        resolver = OpenLibraryResolver()

        for book in self._books:
            if book.isbn == isbn:
                raise ValueError("Eklemeye çalıştığınız kitap zaten mevcut!")
            
        url = f"https://openlibrary.org/isbn/{isbn}.json"

        try:
            response = httpx.get(url, timeout=10, follow_redirects=True)
            response.raise_for_status()  # HTTP hatası varsa exception fırlatır

            data = response.json() # gelen veriyi dict e çevirir

            title = data.get("title")

            if "authors" in data:
                authors = resolver.resolve(data.get("authors")[0].get("key"))
            else:
                authors = None

            if "languages" in data:
                language = resolver.resolve(data.get("languages")[0].get("key"))
            else:
                language = None

            publish_date = data.get("publish_date")
            publishers = data.get("publishers")
            isbn_13 = data.get("isbn_13")[0]


            new_book = Book(title, authors, language, publish_date, publishers, isbn_13)

            self._books.append(new_book)
                # Kitap bilgilerinin kalıcı olarak saklanması için 
            self.save_books()

        except httpx.HTTPStatusError:
                print("Kitap bulunamadı")

        except httpx.RequestError:
            print("Sunucuya ulaşılamadı")



    def remove_book(self, isbn: str):

        for book in self._books:  
            if book.isbn == isbn:
                self._books.remove(book)
                self.save_books()
                return
            
        raise ValueError("There is no such a book!")

    

    def find_book(self, title: str) -> Book:

        for book in self._books:
            if book.title.lower() == title.lower():
                return book
            
        raise ValueError(f"Kitap bulunamadı: {title}")
        
    

    @property
    def total_books(self) -> int:
        return len(self._books)
    

@dataclass
class Manager:
    userName: str
    _password: int






