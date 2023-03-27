from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2 import sql
from fastapi.middleware.cors import CORSMiddleware
import jwt
import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Создаем файловый обработчик логов
file_handler = logging.FileHandler('log')
file_handler.setLevel(logging.INFO)

# Создаем форматтер
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)

# Создание экземпляра приложения FastAPI
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Класс модели данных для хранения информации о пользователе
class User(BaseModel):
    name: str
    email: str
    password: str
    role_id: int

# Параметры подключения к базе данных Postgres
db_name = 'mydb'
db_user = 'myuser'
db_password = 'mypassword'
db_host = 'wtp-db'
db_port = '5432'

# Функция для установления соединения с базой данных Postgres
def get_conn():
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    return conn

def get_user_id(email):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return user_id

# функция для генерации JWT-токена и сохранения его в таблице tokens
def generate_token(email,password):
    conn = get_conn()
    # получаем дату и время сейчас
    now = datetime.datetime.utcnow()
    # устанавливаем время действия токена на 30 минут
    expiration = now + datetime.timedelta(minutes=30)
    # создаем словарь с данными для токена
    token_data = {
        "exp": expiration,
        "iat": now,
        "sub": "access_token",
        "email": email,
        "password": password
    }
    # создаем токен с помощью библиотеки jwt
    token = jwt.encode(token_data, "secretkey", algorithm="HS256")
    # сохраняем токен в таблице tokens
    user = get_user_id(email)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tokens (user_id, token, expire_at) VALUES (%s,%s,%s)", (user, token, expiration))
    conn.commit()
    cursor.close()
    return token

# функция для проверки аутентификации в таблице users
def authenticate_user(email, password):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return True
    else:
        return False

@app.get("/login")
async def login(email: str, password: str):
    logger.info("User login request received with email %s", email)
    # проверяем аутентификацию в таблице users
    authenticated = authenticate_user(email, password)
    if not authenticated:
        logger.error("Authentication failed for user with email %s", email)
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    logger.info("User %s successfully authenticated", email)
    # генерируем токен и возвращаем его
    token = generate_token(email,password)
    logger.info("Access token generated for user %s", email)
    return {"access_token": token}

# Обработчик HTTP-запроса метода POST для создания нового пользователя
@app.post("/users")
async def create_user(user: User):
    # Создание новой записи в базе данных
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email, password, role_id) VALUES (%s, %s,%s, %s)", (user.name, user.email, user.password, user.role_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "User created successfully"}

# Обработчик HTTP-запроса метода GET для получения списка всех пользователей
@app.get("/users")
async def read_users():
    # Получение списка всех записей из базы данных
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # Преобразование списка записей в список словарей
    users = []
    for row in rows:
        user = {"id": row[0], "name": row[1], "email": row[2], "password": row[3], "role_id": [4]}
        #Заложенная бомба для тестеров, возвращается список [4] вместо ответав методе
        #user = {"id": row[0], "name": row[1], "email": row[2], "password": row[3], "role_id": row[4]}
        users.append(user)
    return users

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    conn = get_conn()
    cursor = conn.cursor()
    update_query = sql.SQL("""
        UPDATE users SET name = %s, email = %s, password = %s, role_id = %s WHERE id = %s;
    """)
    try:
        cursor.execute(update_query, (user.name, user.email, user.password, user.role_id, user_id))
        conn.commit()
    except:
        raise HTTPException(status_code=404, detail="User not found")
    finally:
        cursor.close()
        conn.close()
    return {"message": "User updated successfully"}

@app.patch("/users/{user_id}")
def partial_update_user(user_id: int, user: User):
    conn = get_conn()
    cursor = conn.cursor()
    update_query = sql.SQL("""
        UPDATE users SET name = %s, email = %s, password = %s, role_id = %s WHERE id = %s;
    """)
    try:
        cursor.execute(update_query, (user.name, user.email, user.password, user.role_id, user_id))
        conn.commit()
    except:
        raise HTTPException(status_code=404, detail="User not found")
    finally:
        cursor.close()
        conn.close()
    return {"message": "User updated successfully"}

#Метод не срабатывает коректно
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"User with id {user_id} has been deleted."}


