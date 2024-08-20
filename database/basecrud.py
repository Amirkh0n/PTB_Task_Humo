import sqlite3
from abc import ABC, abstractmethod
from contextlib import closing


class BaseCRUD(ABC):
    def __init__(self, database_path, table_name):
        self.database_path = database_path
        self.table_name = table_name

    
    def get_connection(self):
        return closing(sqlite3.connect(self.database_path))

    def migrate(self):
      with self.get_connection() as connection:
        cursor = connection.cursor()
        # Jadval yaratish
        queries = [
            '''
            CREATE TABLE IF NOT EXISTS users(
              user_id INTEGER PRIMARY KEY NOT NULL,
              name TEXT, 
              phone_number INTEGER,
              bascet INTEGER ,
              FOREIGN KEY (bascet) REFERENCES orders(id)
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS categories(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL UNIQUE 
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS products (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              description TEXT, 
              image_path TEXT,
              price INTEGER ,
              count INTEGER ,
              category_id INTEGER NOT NULL,
              FOREIGN KEY (category_id) REFERENCES categories(id)
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS orders(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER NOT NULL,
              status TEXT NOT NULL, 
              phone_number INTEGER,
              latitude REAL,
              longitude REAL,
              FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS orderproduct(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              count INTEGER NOT NULL,
              price INTEGER NOT NULL, 
              product_id INTEGER NOT NULL, 
              order_id INTEGER NOT NULL, 
              FOREIGN KEY (product_id) REFERENCES products(id), 
              FOREIGN KEY (order_id) REFERENCES orders(id)
            );
            ''',
        ]

        for query in queries:
            cursor.execute(query)
        
        connection.commit()
        print('Database created!')
    
    def insert(self, **kwargs):
        i=0
        while True: 
            try:
              with self.get_connection() as connection:
                cursor = connection.cursor()
                columns = ', '.join(kwargs.keys())
                placeholders = ', '.join('?' for _ in kwargs)
                query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
                cursor.execute(query, tuple(kwargs.values()))
                connection.commit()
                return cursor.lastrowid
            except sqlite3.OperationalError as e:
                if i>3:
                    print('Xatolik:\n', e)
                    return 
                self.migrate()
                i+=1
            except Exception as e:
                print('Xatolik!!!\n', e)
                return

    def get_all(self):
        i=0
        while True: 
            try:
              with self.get_connection() as connection:
                cursor = connection.cursor()
                query = f"SELECT * FROM {self.table_name}"
                cursor.execute(query)
                return cursor.fetchall()
            except sqlite3.OperationalError:
                if i>3:
                    print('Xatolik:\n' ,sqlite3.OperationalError)
                    return 
                self.migrate()
                i+=1
            except Exception as e:
                print('Xatolik!!!\n', e)
                return
        
    def get(self, id, id_column="id",  all=False):
        i = 0
        while True:
            try:
              with self.get_connection() as connection:
                cursor = connection.cursor()
                query = f"SELECT * FROM {self.table_name} WHERE {id_column}=?"
                cursor.execute(query, (id,))
                if all:
                    return cursor.fetchall()
                return cursor.fetchone()
            except sqlite3.OperationalError:
                if i>3:
                    print('Xatolik:\n' ,sqlite3.OperationalError)
                    return 
                self.migrate()
                i+=1
            except Exception as e:
                print('Xatolik!!!\n', e)
                return

    def get_all_user_id(self):
        i = 0
        while True: 
            try:
              with self.get_connection() as connection:
                cursor = connection.cursor()
                query = f"SELECT user_id FROM users"
                cursor.execute(query)
                return [user[0] for user in cursor.fetchall()]
            except sqlite3.OperationalError:
                if i>3:
                    print('Xatolik:\n' ,sqlite3.OperationalError)
                    return 
                i+=1
                self.migrate()
            except Exception as e:
                print('Xatolik!!!\n', e)
                return
        
    def update(self, id, id_column="id", **kwargs):
        i = 0
        while True: 
            try:
              with self.get_connection() as connection:
                cursor = connection.cursor()
                columns = ', '.join(f"{key}=?" for key in kwargs)
                query = f"UPDATE {self.table_name} SET {columns} WHERE {id_column}=?"
                cursor.execute(query, (*kwargs.values(), id))
                connection.commit()
                return
            except sqlite3.OperationalError:
                if i>3:
                    print('Xatolik:\n' ,sqlite3.OperationalError)
                    return 
                self.migrate()
                i+=1
            except Exception as e:
                print('Xatolik!!!\n', e)
                return

    def delete(self, id, id_column="id"):
        i = 0
        while True: 
            try:
              with self.get_connection() as connection:
                cursor = connection.cursor()
                query = f"DELETE FROM {self.table_name} WHERE {id_column}=?"
                cursor.execute(query, (id,))
                connection.commit()
                return 
            except sqlite3.OperationalError:
                if i>3:
                    print('Xatolik:\n' ,sqlite3.OperationalError)
                    return 
                self.migrate()
                i+=1
            except Exception as e:
                print('Xatolik!!!\n', e)
                return
    
    