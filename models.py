from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, DateTime, BigInteger, Integer, ForeignKey, Boolean
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from database_connection import session, try_session_commit
from fastapi import HTTPException

class Base(DeclarativeBase):
    pass


class MemberBook(Base):
    __tablename__ = 'member_book'
    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    book_id = Column('book_id', String, ForeignKey('books.isbn_number'))

    
class MemberMagazine(Base):
    __tablename__ = 'member_magazine'
    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    magazine_id = Column('magazine_id', String,
                         ForeignKey('magazines.issn_number'))
    
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False)
    date_created = Column(DateTime(), default=datetime.utcnow().date())
    expiry_date = Column(
        DateTime(), default=datetime.utcnow().date() + timedelta(days=60))
    address = Column(String(200), nullable=False)
    phone_number = Column(BigInteger())
    fine = Column(Integer, default=0)
    book_id = relationship(
        'Book', secondary='member_book', back_populates='user_id')
    magazine_id = relationship(
        'Magazine', secondary='member_magazine', back_populates='user_id')
    record = relationship('Record', backref='user')
    
    
    def get_all(self):
        return session.query(User).all()
    
    def get_from_username(self, username):
        user_object =  session.query(User).where(User.username==username).one_or_none()
        if not user_object:
            raise HTTPException(status_code=404,
                detail= {
                    "error":{
                        "error_type": "Request Not Found",
                        "error_message": f"No User with the Username {username}"
                        }
                    })
        return user_object
    
    def add(self,username,email, address, phone_number):
        session.add(User(
            username=username,
            email=email,
            address=address,
            phone_number=phone_number
            ))
        try:
            session.commit()
            return "User Added Sucessfully"
        except IntegrityError:
            session.rollback()
            # return "Same User Already Exsist"
            raise HTTPException(status_code=400,
                detail= {
                    "error":{
                        "error_type": "Bad Request",
                        "error_message": f"User with username {username} already exsist."
                        }
                    })
    
            
class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    address = Column(String(200))
    phone_number = Column(BigInteger())
    books = relationship('Book', backref='publisher')
    magazine = relationship('Magazine', backref='publisher')
    
    def get_all(self):
        return session.query(Publisher).all()
    
    def get_from_id(self, id):
        return session.query(Publisher).where(Publisher.id == id).one_or_none()
    
    def add(self, name, phone_number, address):
        session.add(Publisher(name=name,address=address,phone_number=phone_number)) 
        try:
            session.commit()
            return "Publisher Added Sucessfully"
        
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=400,
                detail= {
                    "error":{
                        "error_type": "Bad Request",
                        "error_message": f"Publisher named {name} already exsist."
                        }
                    })


class Book(Base):
    __tablename__ = 'books'
    isbn_number = Column(String(15), nullable=False,
                         unique=True, primary_key=True, autoincrement=False)
    title = Column(String(100), nullable=False)
    author = Column(String(20), nullable=False, default='Folklore')
    price = Column(Integer(), nullable=False)
    user_id = relationship(
        'User', secondary='member_book', back_populates='book_id')
    genre_id = Column(Integer(), ForeignKey('genre.id'))
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    available_number = Column(Integer, default=0)
    record = relationship('Record', backref='book')
    
    
    def get_all(self):
        books = session.query(Book).all()
        return books
    
    def get_from_id(self, isbn):
        return session.query(Book).where(Book.isbn_number == str(isbn)).one_or_none()
    
    def add(self,isbn,author,title,price,genre_id,publisher_id,available_number):
        session.add(Book(
                isbn_number=isbn,
                author=author,
                price=price,
                title=title,
                genre_id = genre_id,
                publisher_id= publisher_id,
                available_number = available_number
                ))

        try:
            session.commit()
            return "Book Added Sucessfully"
        except IntegrityError as e:
            # print(e)
            session.rollback()
            # return "The Same Book Already exsist"
            raise HTTPException(status_code=400,
                detail= {
                    "error":{
                        "error_type": "Bad Request",
                        "error_message": f"Book with ISBN number {isbn} already exsist."
                        }
                    })
        
        
class Magazine(Base):
    __tablename__ = 'magazines'
    issn_number = Column(String(15), nullable=False,
                         unique=True, primary_key=True, autoincrement=False)
    title = Column(String(100), nullable=False)
    editor = Column(String(20), nullable=False, default='Folklore')
    price = Column(Integer(), nullable=False)
    user_id = relationship(
        'User', secondary='member_magazine', back_populates='magazine_id')
    genre_id = Column(Integer(), ForeignKey('genre.id'))
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    available_number = Column(Integer, default=0)
    record = relationship('Record', backref='magazine')
    
    def get_all(self):
        return session.query(Magazine).all()
    
    def get_from_id(self, issn):
        return session.query(Magazine).where(Magazine.issn_number == str(issn)).one_or_none()
    
    def add(self,issn,editor,title,price,genre_id,publisher_id,available_number):
        session.add(Magazine(
                issn_number=issn,
                editor=editor,
                price=price,
                title=title,
                genre_id = genre_id,
                publisher_id= publisher_id,
                available_number = available_number
                ))

        try:
            session.commit()
            return "Magazine Added Sucessfully"
        except IntegrityError as e:
            # print(e)
            session.rollback()
            # return "The Same Magazine Already exsist"
            raise HTTPException(status_code=400,
                detail= {
                    "error":{
                        "error_type": "Bad Request",
                        "error_message": f"Magazine with ISSN number {issn} already exsist."
                        }
                    })
    

class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    books = relationship('Book', backref='genre')
    magazine = relationship('Magazine', backref='genre')
    record = relationship('Record', backref='genre')
    
    
    def get_all(self):
        return session.query(Genre).all()
    
    
    def get_from_id(self, id):
        return session.query(Genre).where(Genre.id == id).one_or_none()
    
    def add(self,name):
        session.add(Genre(name=name))
        try:
            session.commit()
            return "Genre Added Sucessfully"
        except IntegrityError:
            session.rollback()
            # return "Same Genre Already Exsist"
            raise HTTPException(status_code=400,
                detail= {
                    "error":{
                        "error_type": "Bad Request",
                        "error_message": f"Genre with name {name} already exsist."
                        }
                    })
    
class Librarian(Base):
    __tablename__ = 'librarians'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    address = Column(String(200), nullable=False)
    phone_number = Column(BigInteger())
    
    def get_all(self):
        result = session.query(
            Librarian.id, 
            Librarian.name, 
            Librarian.email
        ).all()
        return [dict(id=row[0], name=row[1], email=row[2]) for row in result]
    
    def validate_librarian(self, email:str,password:str):
        return session.query(Librarian).where(Librarian.email==email, Librarian.password == password).one_or_none()
    
    
    def user_add_book(self,username, isbn_number, days=15):
        book_to_add = session.query(Book).where(
            Book.isbn_number == isbn_number).one_or_none()
        if not book_to_add:
            raise HTTPException(status_code=404,
                detail= {
                    "error":{
                        "error_type": "Request Not Found",
                        "error_message": f"No Book with the ISBN number {isbn_number}"
                        }
                    })
        
        user_object = User.get_from_username(User,username)
        
        user_object.book_id += [book_to_add]
        book_to_add.available_number -= 1
        user_already_exsist = session.query(Record).where(
            Record.book_id == book_to_add.isbn_number,
            Record.member_id == user_object.id,
            Record.returned == False
        ).count()
        if not user_already_exsist and book_to_add.available_number > 0:
            book_record = Record(
                user=user_object, book=book_to_add,
                genre=book_to_add.genre, issued_date=datetime.utcnow().date(),
                expected_return_date=(
                    datetime.utcnow().date() + timedelta(days=days))
            )
            session.add(book_record)
            try_session_commit(session)
        elif book_to_add.available_number == 0:
            # return CustomDatabaseException(
            #     "This book is curently out of stock, please check again after some days.")
            raise HTTPException(status_code=409,
                detail= {
                    "error":{
                        "error_type": "Insufficient Resources",
                        "error_message": "This book is curently out of stock, please check again after some days."
                        }
                    })

        else:
            raise HTTPException(status_code=400,
                detail= {
                    "error":{
                        "error_type": "Bad Request",
                        "error_message": "You have already issued this same book already."
                        }
                    })
    
    
    def user_return_book(self,username, isbn_number):

            book_to_return = session.query(Book).where(
                Book.isbn_number == isbn_number).one_or_none()
            if not book_to_return:
                
                raise HTTPException(status_code=404,
                detail= {
                    "error":{
                        "error_type": "Request Not Found",
                        "error_message": f"No Book with the ISBN number {isbn_number}"
                        }
                    })
            user_object = User.get_from_username(User,username)
            got_record = session.query(Record).where(
                Record.member_id == user_object.id,
                Record.book_id == isbn_number,
                Record.returned == False
            ).one_or_none()
            fine = 0
            if got_record:
                books_record = session.query(Record).filter(
                    Record.member_id == user_object.id,
                    Record.book_id == isbn_number,
                    Record.returned == False
                ).one()
                if books_record.expected_return_date.date() < datetime.utcnow().date():

                    extra_days = (datetime.utcnow().date() -
                                  books_record.expected_return_date.date()).days
                    if extra_days > 3:
                        fine = extra_days * 3
                book_to_return.available_number += 1
                books_record.returned = True
                books_record.returned_date = datetime.utcnow().date()
                session.query(MemberBook).filter(
                    MemberBook.book_id == isbn_number,
                    MemberBook.user_id == user_object.id
                ).delete()
                try_session_commit(session)
                return fine

            else:
                raise HTTPException(status_code=404,
                detail= {
                    "error":{
                        "error_type": "Request Not Found",
                        "error_message": f"User {username} haven't borrowed {book_to_return.title}"
                        }
                    })
                
                
    def user_return_magazine(self, username, issn_number):
        
        magazine_to_return = session.query(Magazine).where(
            Magazine.issn_number == issn_number).one_or_none()

        if not magazine_to_return:
            raise HTTPException(status_code=404,
                detail= {
                    "error":{
                        "error_type": "Request Not Found",
                        "error_message": f"No Magazine with the ISSN number {issn_number}"
                        }
                    })
            
        user_object = User.get_from_username(User, username)
        got_record = session.query(Record).where(
            Record.member_id == user_object.id,
            Record.magazine_id == issn_number,
            Record.returned == False
        ).one_or_none()
        fine=0
        if got_record:
            magazine_record = session.query(Record).filter(
                Record.member_id == user_object.id,
                Record.magazine_id == issn_number,
                Record.returned == False
            ).one()
            if magazine_record.expected_return_date.date() < datetime.utcnow().date():

                extra_days = (magazine_record.expected_return_date.date(
                ) - datetime.utcnow().date()).days
                if extra_days > 3:
                    fine = extra_days * 3
                    

            magazine_to_return.available_number += 1
            magazine_record.returned = True
            magazine_record.returned_date = datetime.utcnow().date()

            session.query(MemberMagazine).filter(
                MemberMagazine.magazine_id == issn_number,
                MemberMagazine.user_id == user_object.id
            ).delete()
            try_session_commit(session) 
            return fine
        else:
            raise HTTPException(status_code=404,
                detail= {
                    "error":{
                        "error_type": "Request Not Found",
                        "error_message": f"User {username} haven't borrowed {magazine_to_return.title}"
                        }
                    })
                   
                 
    def user_add_magazine(self,username, issn_number, days=15):
        
        magazine_to_add = session.query(Magazine).where(
            Magazine.issn_number == issn_number).one_or_none()
        if not magazine_to_add:
            raise HTTPException(status_code=404,
                detail= {
                    "error":{
                        "error_type": "Request Not Found",
                        "error_message": f"No Magazine with the ISSN number {issn_number}"
                        }
                    })
        user_object = User.get_from_username(User, username)
        user_object.magazine_id += [magazine_to_add]
        user_already_exsist = session.query(Record).where(
            Record.magazine_id == magazine_to_add.issn_number,
            Record.member_id == user_object.id,
            Record.returned == False
        ).count()
        
        if not user_already_exsist and magazine_to_add.available_number > 0:
            magazine_to_add.available_number -= 1
            magazine_record = Record(
                user=user_object,
                magazine=magazine_to_add,
                genre=magazine_to_add.genre,
                issued_date=datetime.utcnow().date(),
                expected_return_date=(
                    datetime.utcnow().date() + timedelta(days=days))
            )
            session.add(magazine_record)
            try_session_commit(session)
        elif magazine_to_add.available_number == 0:
            raise HTTPException(status_code=409,
                detail= {
                    "error":{
                        "error_type": "Insufficient Resources",
                        "error_message": "This Magazine is curently out of stock, please check again after some days."
                        }
                    })
        else:
            raise HTTPException(status_code=400,
                detail= {
                    "error":{
                        "error_type": "Bad Request",
                        "error_message": "You have already issued this same Magazine already."
                        }
                    })
            

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer(), primary_key=True)
    member_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(String, ForeignKey('books.isbn_number'))
    magazine_id = Column(String, ForeignKey('magazines.issn_number'))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    issued_date = Column(DateTime(), default=datetime.utcnow().date())
    returned_date = Column(DateTime(), default=datetime.utcnow().date())
    expected_return_date = Column(DateTime(), default=(
        datetime.utcnow().date() + timedelta(days=15)))
    returned = Column(Boolean, default=False)