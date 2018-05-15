import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse
import getpass

class PasswordPromptAction(argparse.Action):
    def __init__(self,
             option_strings,
             dest=None,
             nargs=0,
             default=None,
             required=False,
             type=None,
             metavar=None,
             help=None):
        super(PasswordPromptAction, self).__init__(
             option_strings=option_strings,
             dest=dest,
             nargs=nargs,
             default=default,
             required=required,
             metavar=metavar,
             type=type,
             help=help)

    def __call__(self, parser, args, values, option_string=None):
        password = getpass.getpass()
        setattr(args, self.dest, password)


parser = argparse.ArgumentParser()
parser.add_argument('--username', '-u', help='User to log in as', required=True)
parser.add_argument('-p', dest='password', action=PasswordPromptAction, type=str, required=True)
parser.add_argument('--to', '-t', help='Recipient of email', required=True)
parser.add_argument('--subject', '-s', help='Subject of email')
parser.add_argument('--body', '-b', help='Body of email')
args = parser.parse_args()

gmail_user = args.username
gmail_password = args.password
to = args.to

msg = MIMEMultipart()
msg['From'] = gmail_user
msg['To'] = to
msg['Subject'] = args.subject
 
f = open(args.body, "r")
body = f.read()


msg.attach(MIMEText(body, 'plain'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(gmail_user, gmail_password)
text = msg.as_string()
server.sendmail(gmail_user, to, text)
server.quit()
