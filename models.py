from pydantic import BaseModel


class Task(BaseModel):  # Модель задачи
    id: int
    text: str
    description: str
    is_done: bool
    token: str


class Users(BaseModel):  # Модель пользователя
    id: int
    login: str
    token: str
