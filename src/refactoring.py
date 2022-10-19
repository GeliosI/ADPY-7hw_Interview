from imaplib import IMAP4_SSL
from smtplib import SMTP
from email import message_from_string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailClient:
    def __init__(self, mail_smtp, mail_imap):
        self.MAIL_SMTP = mail_smtp
        self.MAIL_IMAP = mail_imap

    def send_message(self, from_addr, to_addrs, subject, msg_text, passwd, smtp_port):
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = ', '.join(to_addrs)
        msg['Subject'] = subject
        msg.attach(MIMEText(msg_text))

        smtp_obj = SMTP(self.MAIL_SMTP, smtp_port)
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.ehlo()
        smtp_obj.login(from_addr, passwd)
        sendmail_result = smtp_obj.sendmail(from_addr, to_addrs, msg.as_string())
        smtp_obj.quit()
        return sendmail_result

    def recieve_message(self, from_addr, passwd, header=None):
        mail = IMAP4_SSL(self.MAIL_IMAP)
        mail.login(from_addr, passwd)
        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = message_from_string(raw_email)
        mail.logout()
        return email_message


if __name__ == '__main__':
    my_mail = MailClient("smtp.gmail.com", "imap.gmail.com")

    my_mail.send_message(
        from_addr='login@gmail.com',
        to_addrs=['vasya@email.com', 'petya@email.com'],
        subject='Subject',
        msg_text='msg_text',
        passwd='qwerty',
        smtp_port='587'
    )

    my_mail.recieve_message(
        from_addr='login@gmail.com',
        passwd='qwerty'
    )