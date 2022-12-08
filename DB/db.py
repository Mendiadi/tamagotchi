import dataclasses
import json
import sqlite3



@dataclasses.dataclass
class SaveProgress:
    id:int
    level:int
    evolution:int
    coins:int
    inventory:dict
    time:str
    name: str


    def pack(self):
        cols = []
        values = []
        for key,val in self.__dict__.items():
            if key == "id":
                continue
            if key == "inventory":
                val = json.dumps(val)
            cols.append(key)
            values.append(f"\'{str(val)}\'")
        print(cols,values)
        return cols,values

class DB:

    def __init__(self):
        db = sqlite3.connect(f"../tamagochi.db")
        cursor = db.cursor()

        cursor.execute("create  table if not exists game_saves (id integer primary key autoincrement,"
                       "level integer,evolution integer,coins integer,"
                       "inventory varchar(1000),time varchar(50),name varchar(50) unique);")
        db.commit()
        cursor.close()
        db.close()

    def add_save(self, save):
        if not save:
            return
        db = sqlite3.connect("../tamagochi.db")
        cursor = db.cursor()
        col, vals = save.pack()
        print(f"insert into game_saves ({','.join(col)}) values ({','.join(vals)});")
        cursor.execute(f"insert into game_saves ({','.join(col)}) values ({','.join(vals)});")

        db.commit()
        cursor.close()
        db.close()

    def delete(self,save):
        db = sqlite3.connect("../tamagochi.db")
        cursor = db.cursor()
        cursor.execute(f"delete from game_saves where id = {save.id};")
        db.commit()
        cursor.close()
        db.close()

    def get_save(self,save):
        if not save:
            return
        db = sqlite3.connect("../tamagochi.db")
        cursor = db.cursor()
        cursor.execute(f"select from game_saves where id = {save.id} and name = {save.name};")
        db.commit()
        data = cursor.fetchone()
        cursor.close()
        db.close()
        return data

    def update_save(self,save):
        db = sqlite3.connect("../tamagochi.db")
        cursor = db.cursor()
        col, vals =  save.pack()
        res = []
        for i in range(len(col)):
            res.append(f"{col} = {vals}")
        cursor.execute(f"update table game_saves ({','.join(res)});")
        db.commit()
        cursor.close()
        db.close()


    def get_all_saves(self):
        db = sqlite3.connect("../tamagochi.db")
        cursor = db.cursor()
        cursor.execute(f"select * from game_saves;")

        saves = []
        for data in cursor.fetchall():
             saves .append(SaveProgress(data[0],data[1],data[2],data[3],
                            json.loads(data[4]),data[5],data[6]))
        cursor.close()
        db.close()
        return saves
