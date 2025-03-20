from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from datetime import date, datetime
from models import User
from tortoise.contrib.fastapi import register_tortoise


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tests-tasks.onrender.com/", "http://localhost:5173/", "http://tests-tasks.onrender.com/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str
    username: str
    birth_date: date

@app.post("/user/")
async def create_user(user: UserCreate):
    print(f"НОвый {user}")
    user_obj = await User.create(
        telegram_id=user.telegram_id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        birth_date=user.birth_date,
    )
    return {"id": user_obj.id}

@app.get("/user/{username}")
async def get_user(username: str):
    users = await User.filter(username=username)
    if users:
        return users[0]
    raise HTTPException(status_code=444, detail="User not found")

@app.get("/user/{username}/birthday")
async def get_birthday_countdown(username: str):
    users = await User.filter(username=username)
    if not users:
        raise HTTPException(status_code=404, detail="User not found")

    user = users[0]

    today = date.today()
    next_birthday = date(today.year, user.birth_date.month, user.birth_date.day)
    if next_birthday < today:
        next_birthday = date(today.year + 1, user.birth_date.month, user.birth_date.day)

    delta = next_birthday - today
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    print("Response Data:", user, days, hours, minutes)
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "days_until_birthday": days,
        "hours_until_birthday": hours,
        "minutes_until_birthday": minutes,
    }

register_tortoise(
    app,
    db_url="postgres://:@:/",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
