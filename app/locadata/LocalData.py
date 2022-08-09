import sqlite3
from typing import Tuple

pseudo_db = [
    ("admin" , "$2b$06$7lGrHO0GVMJuPTVhNNMeneyfc3DNd1Q1Ovp4vI/IhuMT2rUiEbWt6" )
]

class LocalDB:

    db_connection : sqlite3.Connection
    db_cursor : sqlite3.Cursor

    def __init__(self) -> None:
        self.init_db()
        pass

    #---- METHODS ----
    def init_db(self):
        self.db_connection = sqlite3.connect("my_local.db")
        self.db_cursor = self.db_connection.cursor()

        try:
            self.db_cursor.execute(
                    '''
                    CREATE TABLE users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(24),
                        phone VARCHAR(60) UNIQUE,
                        password VARCHAR(60)
                    );
                    '''
            )
            self.db_cursor.execute(
                    '''
                    CREATE TABLE orders(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_id INTEGER,
                        details TEXT,
                        total REAL,
                        FOREIGN KEY (client_id) REFERENCES users(id)
                    );
                    '''
                )
        except:
            pass
    
    
    def create_user(self, name: str , phone : str , password : str) -> int:
        self.db_cursor.execute(
            '''
            INSERT INTO users VALUES (null ,? ,? ,? )
            ''', [name , phone , password]
        )
        self.db_connection.commit()

        self.db_cursor.execute(
            '''
            SELECT * FROM users WHERE phone = ?
            ''', [phone])
        fetched = self.db_cursor.fetchone()
        return fetched[0]
    
    def get_user_from_db(self, phone : str) -> tuple|None:
        self.db_cursor.execute(
            '''
            SELECT * FROM users WHERE phone = ?
            ''', [phone]
        )
        return self.db_cursor.fetchone()

    def get_user_by_id(self, id : int) -> tuple|None:
        self.db_cursor.execute(
            '''
            SELECT * FROM users WHERE id = ?
            ''', [id])
        return self.db_cursor.fetchone()


# --- FACTORY ---

def get_db_instance( instance = LocalDB()) -> LocalDB:
    return instance


