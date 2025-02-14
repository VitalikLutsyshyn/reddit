from app import *


with app.app_context():#створення таблиці в базі даних
    #db.drop_all() #видалення усіх таблиць

    db.create_all()