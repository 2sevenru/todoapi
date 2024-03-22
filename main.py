from typing import Union

import uvicorn
from fastapi import FastAPI, Response, Header

from data.database import Database

database = Database()

app = FastAPI(
    title='ToDoAPI',
    version='1.0',
    docs_url='/api/v1',
    redoc_url='/api/v2'
)


@app.get("/", status_code=200)  # Проверка соединения с API
async def check_connection():
    return {'result': True, "message": "Connection OK"}


@app.get("/tasks/", status_code=200)  # Получение всех задач
async def get_tasks(response: Response, skip: int = 0, limit: int = 20, token: str = Header()):
    validate = await database.validate_token(token)
    if not validate:
        response.status_code = 401
        return {'result': False, 'message': 'Unauthorized'}
    tasks = await database.get_all_tasks(token)
    return {'result': True, 'tasks': tasks[skip: skip + limit]}


@app.post('/tasks/', status_code=201)  # Добавление задачи
async def create_task(response: Response, text: str, description: str, token: str = Header()):
    validate = await database.validate_token(token)
    if not validate:
        response.status_code = 401
        return {'result': False, 'message': 'Unauthorized'}
    task = await database.add_task(text, description, token)
    return {'result': True, 'task': task}


@app.get("/tasks/{task_id}", status_code=200)  # Получение задачи по ID
async def read_task(task_id: int, response: Response, token: str = Header()):
    validate = await database.validate_token(token)
    if not validate:
        response.status_code = 401
        return {'result': False, 'message': 'Unauthorized'}
    task = await database.get_task(task_id, token)
    if task is None:
        response.status_code = 404
        return {'result': False, 'message': 'Task not found'}
    return {'result': True, "task": task}


@app.put("/tasks/{task_id}", status_code=201)  # Обновление text или description по ID задачи
async def update_task(task_id: int, response: Response, text: Union[str, None] = None,
                      description: Union[str, None] = None, token: str = Header()):
    validate = await database.validate_token(token)
    if not validate:
        response.status_code = 401
        return {'result': False, 'message': 'Unauthorized'}

    if text is None and description is None:
        response.status_code = 400
        return {'result': False, "message": "No data provided"}

    task = await database.get_task(task_id, token)
    if task is None:
        response.status_code = 404
        return {'result': False, 'message': 'Task not found'}

    if text is not None:
        await database.update_text_task(task_id, text, token)

    if description is not None:
        await database.update_description_task(task_id, description, token)

    task = await database.get_task(task_id, token)
    return {'result': True, 'task': task}


@app.delete('/tasks/{task_id}', status_code=200)  # Удаление задачи по ID
async def delete_task(task_id: int, response: Response, token: str = Header()):
    validate = await database.validate_token(token)
    if not validate:
        response.status_code = 401
        return {'result': False, 'message': 'Unauthorized'}

    task = await database.get_task(task_id, token)
    if task is None:
        response.status_code = 404
        return {'result': False, 'message': 'Task not found'}
    await database.delete_task(task_id, token)
    return {'result': True}


@app.put("/tasks/done/{task_id}", status_code=201)  # Установка задачи как выполненной по ID
async def update_done_task(task_id: int, response: Response, token: str = Header()):
    validate = await database.validate_token(token)
    if not validate:
        response.status_code = 401
        return {'result': False, 'message': 'Unauthorized'}

    task = await database.get_task(task_id, token)
    if task is None:
        response.status_code = 404
        return {'result': False, 'message': 'Task not found'}

    await database.update_done_task(task_id, token)
    task = await database.get_task(task_id, token)
    return {'result': True, 'task': task}


@app.post('/users/create', status_code=201)
async def create_user(login: str):
    user = await database.create_user(login)
    return {'result': True, 'user': user}


@app.get('/users/get', status_code=200)
async def get_user(response: Response, token: str = Header()):
    validate = await database.validate_token(token)
    if not validate:
        response.status_code = 401
        return {'result': False, 'message': 'Unauthorized'}

    user = await database.get_user_by_token(token)
    return {'result': True, 'user': user}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
