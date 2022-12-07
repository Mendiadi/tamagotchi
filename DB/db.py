import sqlite3


class DB:

    def __init__(self):
        db = sqlite3.connect("tamagochi")
        cursor = db.cursor()
        cursor.execute("create table save id integer primary key autoincrement,life_bar integer,happy integer,"
                       "food_bar integer,age integer,evolution integer")
        db.commit()
        cursor.close()
        db.close()

    def add_save(self, save):
        db = sqlite3.connect("tamagochi")
        cursor = db.cursor()
        cursor.execute(f"insert into save {','.join(save)}")
        db.commit()
        cursor.close()
        db.close()

    def delete(self,save):
        db = sqlite3.connect("tamagochi")
        cursor = db.cursor()
        cursor.execute(f"delete from save where id = {save.id}")
        db.commit()
        cursor.close()
        db.close()