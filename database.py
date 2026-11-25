import sqlite3
DB_NAME = "tasks.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)#فتحت الاتصال مع لقاعده    
    conn.row_factory = sqlite3.Row  # حتى نقدر نوصل للأعمدة بالاسم مثل row["title"]
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()#كورسر اداه بتبعت اوامر للقاعده وبتستقبل

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            priority INTEGER NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)
    cursor.execute(""" CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed) """)
    
    conn.commit()
    conn.close()