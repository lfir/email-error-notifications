import io
import os
import unittest
from os import remove
from unittest.mock import Mock, patch

from dotenv import load_dotenv
from mail_error_notifs.mail_error_notifs import SendGridAPIClient, send_email


class TestScripts(unittest.TestCase):
    testenvpath = "./tests/.testenv"

    def test_when_env_file_present_environment_variables_can_be_read(self):
        with open(TestScripts.testenvpath, "w") as fh:
            fh.write("LOGDIR=/root")

        load_dotenv(TestScripts.testenvpath)

        self.assertIsNotNone(os.getenv("LOGDIR"))

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_when_email_sent_then_statuscode_printed_is_the_one_returned_by_sendgridclient(
        self, mock_stdout
    ):
        SendGridAPIClient.send = Mock()
        send_email("TestCase subject", "TestCase body")

        self.assertIn("SendGrid response status", mock_stdout.getvalue())

    def test_when_email_not_sent_then_error_is_logged(self):
        err_msg = "Send mail error"

        def mockinit(self, apikey):
            raise RuntimeError(err_msg)

        sendgridmock = patch.object(SendGridAPIClient, "__init__", mockinit)

        with sendgridmock, self.assertLogs() as cm:
            send_email("TestCase subject", "TestCase body")

            self.assertIn(err_msg, " ".join(cm.output))

    @classmethod
    def tearDownClass(cls):
        remove(TestScripts.testenvpath)
