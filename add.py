from sqlalchemy import create_engine, text


engine = create_engine("sqlite:///instance/avito_clone.db")

alter_db = text("ALTER TABLE users ADD COLUMN password")


with engine.connect() as connection:
    try:
        connection.execute(alter_db)
        connection.commit()
        print("Столбец password успешно добавлен!")
    except Exception as e:
        print(f"Ошибка: {e}")