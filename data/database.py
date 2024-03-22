from pathlib import Path
from random import choice
from string import ascii_lowercase, digits
from typing import List

import aiosqlite

from models import Task, Users


class Database:
    def __init__(self):
        self.path = str(Path(__file__).parent) + '\database.db'  # Установка пути к БД

    async def get_all_tasks(self, token: str) -> List[Task]:  # Взятие всех задач
        all_tasks = []
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT * FROM tasks WHERE token=?", (token,)) as cursor:
                async for row in cursor:
                    task = Task(id=row[0], text=row[1], description=row[3], is_done=row[2], token=row[4])
                    all_tasks.append(task)
        return all_tasks

    async def get_task(self, task_id: int, token: str) -> Task:  # Получение задачи по ID
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT * FROM tasks WHERE id =? and token=?", (task_id, token)) as cursor:
                async for row in cursor:
                    return Task(id=row[0], text=row[1], description=row[3], is_done=row[2], token=row[4])

    async def add_task(self, text: str,
                       description: str, token: str) -> Task:  # Добавление задачи и возвращение её
        async with aiosqlite.connect(self.path) as db:
            cursor = await db.execute(
                "INSERT INTO tasks (text, description, is_done, token) VALUES (?, ?, False, ?)",
                (text, description, token))
            await db.commit()
            return await self.get_task(cursor.lastrowid, token)

    async def update_text_task(self, task_id: int, new_text: str, token: str):  # Обновление текста по ID задачи
        async with aiosqlite.connect(self.path) as db:
            await db.execute("UPDATE tasks SET text =? WHERE id =? and token =?", (new_text, task_id, token))
            await db.commit()

    async def update_description_task(self, task_id: int,
                                      new_description: str, token: str):  # Обновление описания по ID задачи
        async with aiosqlite.connect(self.path) as db:
            await db.execute("UPDATE tasks SET description =? WHERE id =? and token =?",
                             (new_description, task_id, token))
            await db.commit()

    async def update_done_task(self, task_id: int, token: str):  # Установка выполнения задачи по ID
        async with aiosqlite.connect(self.path) as db:
            await db.execute("UPDATE tasks SET is_done = True WHERE id =? and token =?", (task_id, token))
            await db.commit()

    async def delete_task(self, task_id: int, token: str):  # Удаление задачи по ID
        async with aiosqlite.connect(self.path) as db:
            await db.execute("DELETE FROM tasks WHERE id =? and token =?", (task_id, token))
            await db.commit()

    async def validate_token(self, token: str) -> bool:
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT * FROM users WHERE token =?", (token,)) as cursor:
                row = await cursor.fetchone()
                return True if row else False


    async def generate_token(self) -> str:
        token = ''
        for i in range(1, 21):
            token += choice(ascii_lowercase + digits)
            if i in (5, 10, 15):
                token += '-'

        if await self.validate_token(token):
            return await self.generate_token()

        return token

    async def get_user_by_id(self, user_id: int) -> Users:
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT * FROM users WHERE id =?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                return Users(id=row[0], login=row[1], token=row[2])


    async def create_user(self, login: str) -> Users:
        token = await self.generate_token()
        async with aiosqlite.connect(self.path) as db:
            cursor = await db.execute("INSERT INTO users (login, token) VALUES (?, ?)", (login, token))
            await db.commit()
            return await self.get_user_by_id(cursor.lastrowid)

    async def get_user_by_token(self, token: str) -> Users:
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT * FROM users WHERE token =?", (token,)) as cursor:
                row = await cursor.fetchone()
                return Users(id=row[0], login=row[1], token=row[2])
