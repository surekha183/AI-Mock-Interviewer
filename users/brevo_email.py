import os
from sib_api_v3_sdk import Configuration, ApiClient
from sib_api_v3_sdk.api.transactional_emails_api import TransactionalEmailsApi
from sib_api_v3_sdk.models import SendSmtpEmail


def send_brevo_email(to_email, subject, html_content):
    configuration = Configuration()
    configuration.api_key["api-key"] = os.getenv("BREVO_API_KEY")

    api_instance = TransactionalEmailsApi(ApiClient(configuration))

    send_smtp_email = SendSmtpEmail(
        sender={
            "name": "MockMate AI",
            "email": os.getenv("DEFAULT_FROM_EMAIL"),
        },
        to=[{"email": to_email}],
        subject=subject,
        html_content=html_content,
    )

    api_instance.send_transac_email(send_smtp_email)