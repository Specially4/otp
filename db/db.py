from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session


# подлючение
sql_db = "sqlite:///otp.db"

engine = create_engine(sql_db)


class Base(DeclarativeBase): pass


class Person(Base):
    """
    :param name: имя пользователя
    :param hash_secret: зашифрованный секретный ключ
    :param path_to_qrcode: Путь до файла с изображением QR-кода
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    secret = Column(String)
    issuer_name = Column(String)


Base.metadata.create_all(bind=engine)

def save_user(user: Person):
    with Session(autoflush=False, bind=engine) as db:
        db.add(user)
        db.commit()

def search_user(name: str) -> Person | None:
    with Session(autoflush=False, bind=engine) as db:
        user = db.query(Person).filter(Person.name == name).first()
        return user
