import os
from validators import User
import smtplib
from email.mime.text import MIMEText
from constant import user_data_template
import json
from redis_client import RedisConnectionManager


async def get_user(user_id: str) -> User:
    redis = await RedisConnectionManager.get_or_create_connection()
    user_data = json.loads(await redis.get(user_id) or '{}')
    user_data.update(id=user_id)
    return User(**user_data)

async def save_user(user: User):
    redis = await RedisConnectionManager.get_or_create_connection()
    await redis.set(name=user.id, value=user.model_dump_json())


def send_user_request(user: User):
    sender_email = os.getenv('sender_email')
    recipient_email = os.getenv('recipient_email')
    subject = f'Новая заявка от компании {user.company}'
    body = user_data_template.format(**user.model_dump())
    application_password = os.getenv('email_password')
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    with smtplib.SMTP('smtp.mail.ru', 587) as server:
        server.starttls()
        server.login(user=sender_email, password=application_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())


def code_str(s: str) -> str:
    return f'<code>{s}</code>'


def code_user(user: User) -> dict:
    return {key: code_str(value) for key, value in user.model_dump().items()}
