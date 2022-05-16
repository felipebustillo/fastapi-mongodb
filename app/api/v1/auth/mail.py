from sendgrid.helpers.mail import Mail

from app.api.v1.users.models import User
from app.core.config import sendgrid_client, settings


async def send_verification_email(user: User):
    token = "1234"
    url = settings.HOST + settings.API_V1_STR + "/auth/verify" + token
    message = Mail(
        from_email="noreply@hanka.ai",
        to_emails=user.email,
    )
    message.dynamic_template_data = {
        "subject": "Verify your email",
        "first_name": user.first_name,
        "url": url
    }
    message.template_id = "d-15a792de88d944d8af39e39d76cb2dda"
    response = sendgrid_client.send(message)
    try:
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
