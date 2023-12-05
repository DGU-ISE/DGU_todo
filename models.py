import sqlite3

conn = sqlite3.connect('database.db')

cur = conn.cursor()

def create():
    cur.execute("""CREATE TABLE User(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT, password TEXT,
                nickname TEXT,
                name TEXT,
                picture TEXT,
                motto TEXT 
                )""")
    
    cur.execute("""CREATE TABLE Category(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                user_id INTEGER,
                FOREIGN KEY('user_id') REFERENCES User (id)
                )""")
    
    cur.execute("""CREATE TABLE Todo(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                isComplete INTEGER,
                category_id INTEGER,
                FOREIGN KEY('category_id') REFERENCES Category (id)
                )""")
    

create()
conn.commit()
conn.close()