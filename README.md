## Email error notifications
[![](https://github.com/Asta1986/email-error-notifications/actions/workflows/ci.yml/badge.svg)](https://github.com/Asta1986/email-error-notifications/actions/workflows/ci.yml)

Script that can be used as a scheduled task to send email notifications when certain websites aren't available.

Emails are sent using [Sendgrid](https://sendgrid.com)'s service.

**Additional files used not in VCS:**
- .env

Specific or sensitive information is read from this file, such as Sendgrid's API key and the URL of target websites.

- mail_error_notifs.log

Where exceptions that occur during the execution of the script are logged to.
The directory where the file should be stored is read from the environment variable LOGDIR, that can be set in the first file.
