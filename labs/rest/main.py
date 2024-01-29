from fastapi import FastAPI
from .models import TodoItem

app = FastAPI()

todos = []


@app.post("/todos/")
async def create_todo(todo: TodoItem):
    todos.append(todo)
    return todo


@app.get("/todos/")
async def get_todos():
    return todos


@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return {"error": "Todo not found"}


@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo: TodoItem):
    for i, t in enumerate(todos):
        if t.id == todo_id:
            todos[i] = todo
            return todo
    return {"error": "Todo not found"}


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for i, t in enumerate(todos):
        if t.id == todo_id:
            del todos[i]
            return {"status": "deleted"}
    return {"error": "Todo not found"}
