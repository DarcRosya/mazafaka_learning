from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, event

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"  # имя таблицы в БД
    id = Column(Integer, primary_key=True, index=True)  # первичный ключ, индекс
    name = Column(String, index=True)  # колонка name с индексом
    description = Column(String, nullable=True)  # необязательное описание
    category_id = Column(Integer, ForeignKey('categories.id', ondelete="CASCADE"))

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

DATABASE_URL = "sqlite:///./test.db"  # URL подключения к локальной SQLite БД

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# Создаём движок для взаимодействия с БД. connect_args для SQLite — отключаем проверку потоков

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# Фабрика сессий для работы с БД (открытие, коммиты, закрытие транзакций)

def init_db():
    Base.metadata.create_all(bind=engine)
    # Создаёт таблицы в базе, если их нет