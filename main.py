from fastapi import FastAPI, HTTPException, status
from models import Task
from database import get_connection, init_db

app = FastAPI()
init_db()
def row_to_task(row) -> Task:
    return Task(
        id=row["id"],
        title=row["title"],
        priority=row["priority"],
        completed=bool(row["completed"]),  
    )


@app.get("/")
def home():
    return {"message": "Hello, FastAPI with SQLite is working!"}


@app.post("/tasks")
def create_task(task: Task):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task.id,))
    if cursor.fetchone() is not None:
        conn.close()
        raise HTTPException(status_code=400, detail="Task ID already exists")

    cursor.execute(
        "INSERT INTO tasks (id, title, priority, completed) VALUES (?, ?, ?, ?)",
        (task.id, task.title, task.priority, int(task.completed)),
    )
    conn.commit()
    conn.close()

    return {"status": "created", "task": task}


@app.get("/tasks")
def get_tasks(completed: bool | None = None, priority: int | None = None):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, title, priority, completed FROM tasks WHERE 1=1"
    params = []

    if completed is not None:
        query += " AND completed = ?"
        params.append(int(completed))

    if priority is not None:
        query += " AND priority = ?"
        params.append(priority)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    tasks_list = [row_to_task(row) for row in rows]
    return {
        "total": len(tasks_list),
        "tasks": tasks_list,
    }


@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, priority, completed FROM tasks WHERE id = ?", (task_id,),)
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return row_to_task(row)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    if updated_task.id != task_id:
        raise HTTPException(  status_code=400, detail="Task ID in body must match path ID"  )

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """ UPDATE tasks SET title = ?, priority = ?, completed = ?  WHERE id = ? """,
        (updated_task.title, updated_task.priority, int(updated_task.completed), task_id),
    )
    conn.commit()
    affected_rows = cursor.rowcount
    conn.close()

    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"status": "updated", "task": updated_task}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, priority, completed FROM tasks WHERE id = ?",(task_id,),)
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    deleted_task = row_to_task(row)
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted", "task": deleted_task}