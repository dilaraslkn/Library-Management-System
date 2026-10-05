from library import Library,Book,AudioBook,EBook,BrailleBook,Manager
from member import Member, MemberManager


def main():
    
    library = Library("City Library")
    library.load_books()

    manager = MemberManager()
    manager.load_members()
    
    manager1 = Manager("user12", 123456)


    def log_in():

        while True:
            userName = input("Kullanıcı adınızı girin: ")
            password = int(input("Şifrenizi girin: "))

            if (manager1.userName == userName and manager1._password == password):
                print("Giriş Başarılı") 
                break
            elif (manager1.userName != userName and manager1._password == password): 
                print("Kullanıcı Adı Hatalı!")
            elif (manager1.userName == userName and manager1._password != password):
                print("Şifre Hatalı!")

            else:
                print("Kullanıcı Adı ve Şifre Hatalı!")
            
    log_in()


    
    
    print("""
    ************************************
    ************************************
          
    WELCOME TO CITY LIBRARY!
    
    ************************************
    ************************************

    """)

   

    while True:
        print("""
    OPERATIONS:
          
    1. Member Operations
    2. Book Operations
    3. Quit
    """)
        operation = input("Select the operation you want to perform: ")

        if (operation == "3"):
            break


    # --- MEMBER OPERATIONS ---
        elif (operation == "1"):
            print("""
    OPERATIONS:
              
    1. Add a Member
    2. Remove a Member by ID
    3. Borrow a Book by ID
    4. Show Borrowed Books by ID
    5. Return a Book by ID
    6. Quit
    """)
        
        
        # Kitap bilgilerini kullanıcıdan alma
            def memberInfo():
                memberName = input("Member Name|Surname: ")
                memberId = int(input("Member ID: "))
                borrowedBooks = []

                member = Member(memberName, memberId, borrowedBooks)
                return member
            
        # Bir döngü içinde işlemleri gerçekleştirme
            while True:

                selected = input("Select the operation you want to perform: ")
            

                if (selected == "6"):
                    break

                elif (selected == "1"):
                    member = memberInfo()
                    manager.add_member(member)
                    print("*** Üye ekleme başarılı ***")

                elif (selected == "2"):
                    memberId = int(input("Member ID: "))
                    manager.remove_member(memberId)
                    print("*** Üye silme başarılı ***")

                elif (selected == "3"):
                    bookTitle = input("Book Title: ")
                    memberId = int(input("Member ID: "))
                    manager.add_borrowed_book_by_id(bookTitle, memberId)
                    print("*** Kitap ödünç verildi ***")

                elif (selected == "4"):
                    memberId = int(input("Member ID: "))
                    manager.show_borrowed_books(memberId)

                elif(selected == "5"):
                    bookTitle = input("Book Title: ")
                    memberId = int(input("Member ID: "))
                    manager.return_book_by_id(bookTitle, memberId)
                    print("*** Kitap iade edildi ***")

                else:
                    raise ValueError("Erroneous Operation!")




    # ---  BOOK OPERATIONS ---
        elif(operation == "2"):
            print("""
    OPERATIONS:
              
    1. Add a Book (manuel)
    2. Add a Book (isbn)              
    3. Remove a Book with ISBN
    4. List Books
    5. Search a Book with Title 
    6. Quit
    """) 
    
        # Kitap türlerine göre nesne oluşturma
            def info():
                print("""
    Book Types:
                  
    1. Printed Book
    2. EBook
    3. Audio Book
    4. Braille Book
    """)

                bookType = input("Book Type: ")

                def common_inputs():
                    name = input("Title: ")
                    authors = input("Authors: ").split(",")
                    language = input("Language: ")
                    publish = input("Publish Year (or None): ")
                    publishers = input("Publishers: ").split(",")
                    isbn = input("ISBN 13: ")
                    return name, authors, language, publish, publishers, isbn
        
                name, authors, language, publish, publishers, isbn = common_inputs() # fonksiyonun içindeki değerlere eşitleme


                if bookType == "1":
                    book = Book(name, authors, language, publish, publishers, isbn)
                    return book

                elif bookType == "2":
                    fileFormat = input("File Format: ")
                    book = EBook(name, authors, language, publish, publishers, isbn, fileFormat)
                    return book

                elif bookType == "3":
                    duration = int(input("Duration (minutes): "))
                    book = AudioBook(name, authors, language, publish, publishers, isbn, duration)
                    return book
                
                elif bookType == "4":
                    ages = (input("Ages: "))
                    book = BrailleBook(name, authors, language, publish, publishers, isbn, ages)
                    return book

                else:
                    print("Invalid book type.")


   
    # Bir döngü içinde işlemleri gerçekleştirme
            while True:
                selected = input("Select the operation you want to perform: ") 


                if selected == "6":
                    break
                
            
                elif selected == "1":
                    book = info()
                    library.add_book(book)
                    print("*** Kitap Ekleme Başarılı ***")

                elif selected == "2":
                    isbn = input("ISBN 13: ")
                    library.add_book_by_isbn(isbn)

                elif selected == "3":
                    isbn = input("ISBN 13: ")
                    library.remove_book(isbn)
                    print("*** Kitap Silme Başarılı ***")

                elif selected == "4":
                    library.list_books()

                elif selected == "5":
                    title = input("Title: ")
                    found_book = library.find_book(title)
                    if found_book:
                        print(f"Bulunan kitap: {found_book.title} by {found_book.authors}\n")

                else:
                    raise ValueError("Erroneous Operation!")




if __name__ == "__main__":
    main()




