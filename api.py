from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from typing import List
from library import Library
from member import MemberManager


# pydantic model oluşturma book sınıfı için
class BookSchema(BaseModel):
    title: str
    authors: Optional[List[str]]
    language: Optional[str]
    publish_date: Optional[str]
    publishers: Optional[List[str]]
    isbn: str

# pydantic model oluşturma member sınıfı için
class MemberSchema(BaseModel):
    name: str
    member_id: int
    borrowed_books: List[BookSchema] = []




app = FastAPI()
lib = Library("City Library")
lib.load_books()
manager = MemberManager()
manager.load_members()

# Kitapları listele
@app.get("/books", response_model=List[BookSchema])
def list_books():
    return [
        BookSchema(
            title=b.title,
            authors=b.authors if isinstance(b.authors, list) else ([b.authors] if b.authors else []),
            language=b.language,
            publish_date=b.publish_date,
            publishers=b.publishers,
            isbn=str(b.isbn)
        ) for b in lib._books
    ]

# Üyeleri listele
@app.get("/members", response_model=List[MemberSchema])
def list_members():
    return [
        MemberSchema(
            name=m.name,
            member_id=m.member_id,
            borrowed_books=[
                BookSchema(
                    title=b.title,
                    authors=b.authors if isinstance(b.authors, list) else ([b.authors] if b.authors else []),
                    language=b.language,
                    publish_date=b.publish_date,
                    publishers=b.publishers,
                    isbn=str(b.isbn)
                ) for b in m.borrowed_books
            ]
        ) for m in manager._members
    ]

# Kitap ekle (örnek: ISBN ile)
@app.post("/books")
def add_book(isbn: str):
    try:
        lib.add_book_by_isbn(isbn)
        return {"message": "Kitap başarıyla eklendi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# isbn ile kitap silme
@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    try:
        lib.remove_book(isbn)
        return {"message": "Kitap başarıyla silindi"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Üye ekle
@app.post("/members")
def add_member(name: str, member_id: int):
    from member import Member
    try:
        member = Member(name, member_id)
        manager.add_member(member)
        return {"message": "Üye başarıyla eklendi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Üyeye kitap ödünç ver
@app.post("/members/{member_id}/borrow")
def borrow_book(member_id: int, title: str):
    try:
        manager.add_borrowed_book_by_id(title, member_id)
        return {"message": "Kitap ödünç verildi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Üyeden kitap iade al
@app.post("/members/{member_id}/return")
def return_book(member_id: int, title: str):
    try:
        manager.return_book_by_id(title, member_id)
        return {"message": "Kitap iade edildi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# üye silme member id ile
@app.delete("/members/{member_id}")
def delete_member(member_id: int):
    try:
        manager.remove_member(member_id)
        return {"message": "Üye başarıyla silindi"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))