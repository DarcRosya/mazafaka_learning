from pydantic import EmailStr
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from src.config.settings import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=465,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_verification_email(email: EmailStr, token: str):
    verification_link = f"http://localhost:8000/auth/verify?token={token}"
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body=f"Please verify your email by clicking on the link: {verification_link}",
        subtype=MessageType.plain
    )
    fm = FastMail(conf)
    await fm.send_message(message)
