from app.definitions.services.email_service_interface import EmailServiceInterface
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from app.config import settings


class EmailService(EmailServiceInterface):
    def send_mail(self, email: str, subject: str, message: str) -> None:
        """
        wrapper around mail any mail service to send emails to clients

        :param email: str - email address of recipient
        :param subject: str - subject of email
        :param message: str - message in plain text
        :return: None
        """
        message = Mail(
            from_email="josephmacleanarhin@outlook.com",
            to_emails=email,
            subject=subject,
            plain_text_content=message,
        )

        try:
            sg = SendGridAPIClient(
                "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"
            )
            response = sg.send(message)
            print(response)
        except Exception as e:
            print(e)
