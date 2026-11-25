Project Description:
A backend REST API for managing tasks, built with Python, FastAPI, Pydantic, and SQLite3.

Features:
- Create a new task (POST /tasks)
- Get all tasks with filtering by completed status and priority (GET /tasks)
- Get a single task by ID (GET /tasks/{task_id})
- Update an existing task (PUT /tasks/{task_id})
- Delete a task (DELETE /tasks/{task_id})
- Data validation using Pydantic models
- Persistent database storage using SQLite3 with indexing for faster queries

Project Files:
- main.py: API endpoints and request handling
- models.py: Pydantic schemas and validation rules
- database.py: SQLite database connection, table creation, and indexes
- requirements.txt: Required Python libraries

How to Run:
1. Install libraries:
   pip install -r requirements.txt

2. Start the server:
   uvicorn main:app --reload

3. Open API documentation in browser:
   http://127.0.0.1:8000/docs