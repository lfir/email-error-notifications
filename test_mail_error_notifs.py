import io
import unittest
from unittest.mock import Mock, patch

from dotenv import load_dotenv

from mail_error_notifs import SendGridAPIClient, send_email


class TestScripts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv('./.env')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_when_email_sent_then_statuscode_printed_is_202(self, mock_stdout):
        send_email('TestCase subject', 'TestCase body')
        self.assertIn('status code: 202', mock_stdout.getvalue())

    def test_when_email_not_sent_then_error_is_logged(self):
        err_msg = 'Send mail error'

        def mockinit(self, apikey):
            raise RuntimeError(err_msg)
        
        sendgridmock = patch.object(SendGridAPIClient, '__init__', mockinit)

        with sendgridmock, self.assertLogs() as cm:
            send_email('TestCase subject', 'TestCase body')
            self.assertIn(err_msg, ' '.join(cm.output))
