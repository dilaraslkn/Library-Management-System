import json
from library import Book,EBook,AudioBook,BrailleBook,Library
from dataclasses import dataclass,field
from typing import List

library = Library("City Library")
library.load_books()

@dataclass
class Member:
    name: str
    member_id: int
    borrowed_books: List[Book] = field(default_factory=list)  # her nesne için ayrı bir boş liste oluştur.




member1 = Member('Dilara Asilkan', 101)
member2 = Member('Ahmet Güzel', 102, [])
member3 = Member('Zeynep Zeyrek', 103, [])



class MemberManager:

    def __init__(self):
        self._members = []


    def load_members(self):

        with open("members.json", "r", encoding="utf-8") as file:
            data_list = json.load(file)


        for data in data_list:

            borrowed_books = []
            common_keys = ("title", "authors", "language", "publish_date", "publishers", "isbn")

            for b in data.get("borrowed_books", []):
                # Kitap nesnesini oluştur
                if "file_format" in b:
                    temp_book = EBook(**{k: b.get(k) for k in common_keys + ("file_format",)})
                elif "duration" in b:
                    temp_book = AudioBook(**{k: b.get(k) for k in common_keys + ("duration",)})
                elif "ages" in b:
                    temp_book = BrailleBook(**{k: b.get(k) for k in common_keys + ("ages",)})
                else:
                    temp_book = Book(**{k: b.get(k) for k in common_keys})

            # Aynı ISBN'li kitap library._books'ta varsa onu kullan
                book_ref = next((bk for bk in library._books if bk.isbn == temp_book.isbn), temp_book)
                borrowed_books.append(book_ref)

            member = Member(
                name=data["name"],
                member_id=data["member_id"],
                borrowed_books=borrowed_books
            )
            self._members.append(member)


    def save_members(self):

        # self._member listesindeki her bir nesneyi sözlüğe dönüştürme
        data_list = []
        for m in self._members:
            member_dict = m.__dict__.copy()
            member_dict["borrowed_books"] = [b.__dict__ if hasattr(b, "__dict__") else b for b in m.borrowed_books]
            data_list.append(member_dict)

        with open("members.json", "w", encoding="utf-8") as file:
            json.dump(data_list, file, ensure_ascii=False, indent=4)


    def add_member(self, member: Member):
    
        if member in self._members:
            raise ValueError("Zaten bir üyeliğiniz var!")
    
    
        self._members.append(member)
        # Üye bilgilerinin kalıcı olarak saklanması için 
        self.save_members() 



    def remove_member(self, member_id: int):

        for member in self._members:  
            if member.member_id == member_id:
                self._members.remove(member)
                self.save_members()
                return
                    
        raise ValueError("There is no such a member!")


    def add_borrowed_book_by_id(self, title: str, member_id: int):

        book = library.find_book(title)

        for member in self._members:
            if member.member_id == member_id:
                member.borrowed_books.append(book)
                book.borrow_book()
                self.save_members()
                library.save_books()
                return  # Eşleşme bulunduysa işlem tamam, çık

        # Eğer döngüde eşleşme bulunamazsa buraya düşer
        raise ValueError("Belirtilen ID'ye sahip üye bulunamadı!")
    


    def return_book_by_id(self, title: str, member_id: int):

        for m in self._members:
            if m.member_id == member_id:
                for book in m.borrowed_books:
                    if book.title.lower() == title.lower():
                        m.borrowed_books.remove(book)
                        book.return_book()
                        self.save_members()
                        library.save_books()
                        return 
                raise ValueError("Bu üyenin böyle bir kitabı yok!") 
            
        raise ValueError("Belirtilen ID'ye sahip üye bulunamadı!")



    def show_borrowed_books(self, member_id: int):

        for m in self._members:
            if m.member_id == member_id:
                print("Kitaplar:")

                for book in m.borrowed_books:
                    print(f"Title: {book.title} | Authors: {book.authors} | ISBN 13: {book.isbn}")
                return m.borrowed_books  # İstersen ekrana yazdırıp ayrıca döndürebilirsin
        raise ValueError("Belirtilen ID'ye sahip üye bulunamadı!")
    


manager1 = MemberManager()



