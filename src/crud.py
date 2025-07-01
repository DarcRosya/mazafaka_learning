from models import Item, Category, SessionLocal

def create_item(name: str, description: str | None, category_id: int):
    with SessionLocal() as db:
        item = Item(name=name, description=description, category_id=category_id)  # создаём объект модели
        db.add(item)  # добавляем в сессию (готовим для записи)
        db.commit()  # подтверждаем изменения в базе
        db.refresh(item)  # обновляем объект (чтобы получить id из базы)
        return item  # возвращаем созданный объект


def get_by_id(model, id: int):
    with SessionLocal() as db:
        return db.query(model).filter(model.id == id).first()
    

def get_items_by_category(category_id: int):
    with SessionLocal() as db:
        return db.query(Item).filter(Item.category_id == category_id).all()

def get_by_field(model, field_name: str, value):
    with SessionLocal() as db:
        field = getattr(model, field_name)
        return db.query(model).filter(field == value).all()

def search_items_by_name(query: str):
    with SessionLocal() as db:
        return db.query(Item).filter(Item.name.ilike(f"%{query}%")).all()


def update_item(item_id: int, name: str | None, description: str | None = None, category_id: int | None = None):
    with SessionLocal() as db:
        item = db.query(Item).filter(Item.id == item_id).first()
        if item:
            if name:
                item.name = name  # меняем имя, если передали
            if description:
                item.description = description  # меняем описание, если есть
            if category_id:
                item.category_id = category_id
            db.commit()  # сохраняем изменения
            db.refresh(item)  # обновляем объект из базы
        return item
    

def delete_item(item_id: int):
    with SessionLocal() as db:
        item = db.query(Item).filter(Item.id == item_id).first()
        if item:
            db.delete(item)  # удаляем из сессии (и базы после коммита)
            db.commit()
        return item
    

def create_category(name: str):
    with SessionLocal() as db:
        category = Category(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category


def get_all_fields(model):
    with SessionLocal() as db:
        return db.query(model).all()


def delete_category(id: int):
    with SessionLocal() as db:
        category = db.query(Category).filter(Category.id == id).first()
        if category:
            db.delete(category)
            db.commit()
        return category