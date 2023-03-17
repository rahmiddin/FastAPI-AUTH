from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from config import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_PASSWORD, EMAIL_USE_SSL

conf = ConnectionConfig(
    MAIL_STARTTLS=False,
    MAIL_FROM=EMAIL_HOST_USER,
    MAIL_USERNAME=EMAIL_HOST_USER,
    MAIL_PASSWORD=EMAIL_HOST_PASSWORD,
    MAIL_PORT=EMAIL_PORT,
    MAIL_SSL_TLS=EMAIL_USE_SSL,
    MAIL_SERVER=EMAIL_HOST,
)


async def send_verification_code_message(recipients: list, jwt: str) -> JSONResponse:

    html = f"""<p>Hi this token for mail verification: </p> {jwt}"""
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=recipients,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
