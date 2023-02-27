import logging
import os
from pathlib import PurePath
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import From, Mail, PlainTextContent, Subject, To


def send_email(subject, mailbody):
    """Sends an email using Sendgrid's service to one or more recipients.
    FROM and TO addresses and SENDGRID_API_KEY need to be available as environment variables.

    Positional arguments:
    subject -- A string with the subject of the email.
    mailbody -- A string with the body of the email. Content type will be text/plain.
    """
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        from_email = From(os.getenv("FROM"), "Chronos Maybelambda")
        to_emails = To(os.getenv("TO"))
        subject = Subject(subject)
        content = PlainTextContent(mailbody)
        mail = Mail(from_email, to_emails, subject, content)

        response = sg.send(mail)
        print("SendGrid response status code:", response.status_code)
        print("SendGrid response body:", response.body)
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    load_dotenv("./.env")
    logging.basicConfig(
        filename=PurePath(os.getenv("LOGDIR")) / "mail_error_notifs.log",
        level=logging.ERROR,
        format="%(asctime)s|%(levelname)s|%(message)s",
    )
    errors = set()
    msg = "URL: {}.\nStatus code: {}.\nMessage: {}."
    req0 = Request(os.getenv("URL0"))
    req1 = Request(os.getenv("URL1"))

    for req in [req0, req1]:
        try:
            urlopen(req)
        except HTTPError as e:
            logging.error(e.geturl() + ": " + str(e))
            errors.add(msg.format(req.full_url, e.code, e.read()))

    if len(errors) > 0:
        send_email("Notification of site errors", "\n\n".join(errors))
