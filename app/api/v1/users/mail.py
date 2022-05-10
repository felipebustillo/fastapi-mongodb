from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.core.config import settings

message = Mail(
    from_email='from_email@example.com',
    to_emails='to@example.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')

sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)


async def send_verification_code():
    response = sendgrid_client.send(message)
    try:
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
