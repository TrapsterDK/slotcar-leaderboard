import sqlite3
from dataclasses import dataclass, field

@dataclass
class User:
    id: int
    name: str
    lap_times: list[tuple[int, int]] = field(default_factory=list)

class Database:
    def __init__(self, name="database.db") -> None:
        self.filename = name
        
        try:
            self.con = sqlite3.connect(name)
        except sqlite3.Error as e:
            print(name)
            raise e
        
        self.c = self.con.cursor()

        self.c.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE
        )""")

        self.c.execute("""CREATE TABLE IF NOT EXISTS times_many ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            time_id INTEGER,

            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (time_id) REFERENCES times (id)
        )""")

        self.c.execute("""CREATE TABLE IF NOT EXISTS times (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lap INTEGER,
            time INTEGER
        )""")

        self.c.execute("CREATE INDEX IF NOT EXISTS times_index ON times (time DESC)")

        self.con.commit()

    def close(self) -> None:
        self.con.close()

    def __enter__(self):
        return self 

    def __exit__(self, exc_type, exc_value, exc_traceback): 
        if exc_type:
            self.con.rollback()
            print(exc_type, exc_value, exc_traceback)
        else:
            self.con.commit()

        self.con.close()

    def reset(self) -> None:
        # get all tables
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.c.fetchall()

        # remove internal sqlite table
        tables.remove(('sqlite_sequence',))

        # delete all tables
        for table in tables:
            self.c.execute(f"DELETE FROM {table[0]}")

        self.con.commit()

    def add_users(self, users: list[str]) -> list[int]:
        return [self.add_user(user) for user in users]

    def add_user(self, name: str) -> int:
        self.c.execute("INSERT INTO users (username) VALUES (?)", (name,))
        self.con.commit()
        return self.c.lastrowid
    
    def add_times(self, user_id: int, lap_times: list[tuple[int, int]]) -> None:
        for lap, time in lap_times:
            self.c.execute("INSERT INTO times (lap, time) VALUES (?, ?)", (lap, time))
            time_id = self.c.lastrowid
            self.c.execute("INSERT INTO times_many (user_id, time_id) VALUES (?, ?)", (user_id, time_id))
        self.con.commit()

    def get_user(self, user_id: int, limit_times: int = 3) -> User:
        self.c.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        name = self.c.fetchone()[0]

        if name is None:
            raise ValueError("User does not exist")

        # select times from user sorted by time
        self.c.execute("SELECT times.lap, times.time FROM times INNER JOIN times_many ON times.id = times_many.time_id WHERE times_many.user_id = ? ORDER BY times.time LIMIT ?", (user_id, limit_times))

        return User(user_id, name, self.c.fetchall())

    def get_users_sorted_by_top_time(self, limit_times: int = 3) -> list[User]:
        # select all users sorted by top time (first time), and any without a time last
        self.c.execute("SELECT users.id FROM users LEFT JOIN times_many ON users.id = times_many.user_id LEFT JOIN times ON times.id = times_many.time_id GROUP BY users.id ORDER BY times.time DESC NULLS LAST") 

        return [self.get_user(user_id, limit_times) for user_id, in self.c.fetchall()]

    def get_last_user(self) -> User:
        self.c.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
        
        if self.c.fetchone() is None:
            raise ValueError("No users in database")

        return self.get_user(self.c.fetchone()[0])

    def get_user_count(self) -> int:
        self.c.execute("SELECT COUNT(*) FROM users")
        return self.c.fetchone()[0]

    def get_users(self) -> list[User]:
        self.c.execute("SELECT id FROM users")
        return [self.get_user(user_id[0]) for user_id in self.c.fetchall()]
    

if __name__ == "__main__":
    with Database("database_03-12-2022.db") as db:
        pass
        # db.add_users(["user1", "user2", "user3"])
        # db.add_times(1, [(1, 100), (2, 200), (3, 300)])
        # db.add_times(2, [(1, 200), (2, 300), (3, 400)])
        # db.add_times(3, [(1, 300), (2, 400), (3, 500)])
        

    