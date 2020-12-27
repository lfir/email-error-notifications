import logging
import os
from urllib import request
from urllib.error import HTTPError

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import From, Mail, PlainTextContent, Subject, To

logging.basicConfig(
    filename='mail_error_notifs.log',
    level=logging.ERROR,
    format='%(asctime)s|%(levelname)s|%(message)s'
)
project_folder = os.path.expanduser('~/Devel/python/email-error-notifications')
load_dotenv(os.path.join(project_folder, '.env'))

def send_email(subject, mailbody):
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        from_email = From(os.getenv('FROM'), 'Chronos Maybelambda')
        to_emails = To(os.getenv('TO'))
        subject = Subject(subject)
        content = PlainTextContent(mailbody)
        mail = Mail(from_email, to_emails, subject, content)
        
        response = sg.send(mail)
        print('Response status code:', response.status_code)
        print('Response body:', response.body)
        #print(response.headers)
    except Exception as e:
        logging.error(e)

errors = set()
msg = 'URL: {}.\nStatus code: {}.\nMessage: {}.'
req0 = request.Request(os.getenv('HV1'))
headers = {os.getenv('H1'): req0.full_url}
req1 = request.Request(url=os.getenv('URL1'), headers=headers)

for req in [req0, req1]:
    try:
        request.urlopen(req)
    except HTTPError as e:
        logging.error(e.geturl() + ': ' + str(e))
        errors.add(msg.format(req.full_url, e.code, e.read()))

if len(errors) > 0:
    send_email('Notification of site errors', '\n\n'.join(errors))
