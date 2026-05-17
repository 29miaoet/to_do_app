import sqlite3

class Todo:
    def __init__(self, file_name):
        self.connection = sqlite3.connect(file_name)
        self.cc = self.connection.cursor()
    def create_db(self, db_name):
        self.db_name = db_name
        self.cc.execute(f"""
        CREATE TABLE IF NOT EXISTS {db_name}(
        id INTEGER PRIMARY KEY,
        task TEXT NOT NULL,
        priority INTEGER NOT NULL
        )
        """)
    def find_task(self, task_name):
        for row in self.cc.execute(f"SELECT task FROM {self.db_name}"):
            if task_name in row:
                return row
        return None
        
    def enter_task(self, task, priority, identity=None):
        if self.find_task(task) != None:
            print("Task already exists!")
        elif identity == None:
            self.cc.execute(f"""
            INSERT INTO {self.db_name} (task, priority) VALUES (\"{task}\", {priority})
            """)
        else:
            self.cc.execute(f"""
            INSERT INTO {self.db_name} (id, task, priority) VALUES ({identity}, \"{task}\", {priority})
            """)
    def show_tasks(self):
        return self.cc.execute(f"SELECT * FROM {self.db_name}")

    def get_row_number(self):
        tasks = self.cc.execute(f"SELECT * FROM {self.db_name}")
        rows = tasks.fetchall()
        return len(rows)

    def change_priority(self, priority_id, new_priority):
        self.cc.execute(f"""
        UPDATE {self.db_name}
        SET priority = {new_priority}
        WHERE id = {priority_id}
        """)

    def remove_task(self, task2remove):
        self.cc.execute(f"DELETE FROM {self.db_name} WHERE id = {task2remove}")

    def commit(self):
        self.connection.commit()

    def close_db(self):
        self.connection.commit()
        self.connection.close()
        

