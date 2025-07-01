from models import init_db
import crud

def main():
    init_db()  # создаём таблицы

    category_one = crud.create_category("Hentai Manga")
    print("Created category:", category_one.id, category_one.name)
    category_two = crud.create_category("Capitals")
    print("Created category:", category_two.id, category_two.name)
    
    item_2 = crud.create_item("Metamorphosis", "A very nice book", category_one.id)
    item_1 = crud.create_item("Kiss X Sis", "Ooooh, I like it", category_one.id)
    item_3 = crud.create_item("Argentina", "Messi, Messi, Ancara Messi", category_two.id)
    item_4 = crud.create_item("Kyiv", "SHEEEEE NE VMERLA UKRAIIIINAAAA", category_two.id)
    print("Created:", item_1.id, item_1.name)
    print("Created:", item_2.id, item_2.name)
    print("Created:", item_3.id, item_3.name)
    print("Created:", item_4.id, item_4.name)

    # Получить все товары одной категории
    mangas = crud.get_items_by_category(category_one.id)
    print(f"All items in category '{category_one.name}':")
    for item in mangas:
        print("-", item.id, item.name, item.description)

    # Обновить товар
    updated_manga = crud.update_item(item_1.id, name="some any hentai manga", description="maybe some clishe genres like time stop, I don't know")
    print("Updated item:", updated_manga.id, updated_manga.name, updated_manga.description)

    # Удалить один товар и одну категорию
    crud.delete_item(item_3.id)
    print(f"Deleted item with id {item_3.id}")
    crud.delete_category(category_two.id)
    print(f"Deleted category with id {category_two.id}")


if __name__ == "__main__":
    main()
