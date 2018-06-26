#!/usr/bin/python
import os
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
import coloredlogs, logging


logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

class EmailClientSMTP:
    def __init__(self,
                 smtp_server,
                 smtp_port,
                 smtp_encryption,  # can be SSL, STARTTLS or PLAIN
                 smtp_user_account,
                 smtp_user_passwd,
                 timeout=15):
        self.fromaddr = smtp_user_account
        self.smtp_server_address = smtp_server
        self.smtp_port = int(smtp_port)
        self.smtp_encryption = smtp_encryption
        self.smtp_user_account = smtp_user_account
        self.smtp_user_passwd = smtp_user_passwd
        self.timeout = timeout    # secconds to connect smtp server

    def is_smtp_ssl(self):
        return self.smtp_encryption.lower() == 'ssl'

    def is_smtp_starttls(self):
        return self.smtp_encryption.lower() == 'starttls'

    def build_outer_msg(self,
                        toaddr,
                        subject,
                        body,
                        format='plain'): # format could be plain or html
        msg = MIMEMultipart()
        msg["Subject"] = Header(subject, 'utf-8')
        msg["From"] = self.fromaddr
        msg["To"] = toaddr
        msg.attach(MIMEText(body, format, 'utf-8'))
        return msg


    def add_attachment(self, outer_msg, path_mime):
        '''
        add file/or mimebase as attache into an outer_msg and return the outer_msg
        '''
        if path_mime is None:
            return outer_msg

        # it is a email mime object
        if isinstance(path_mime, MIMEBase):
            outer_msg.attach(path_mime)
            return outer_msg

        # should be file now
        path = path_mime
        if not os.path.isfile(path):
            return
        filename = os.path.basename(path)
        # Guess the content type based on the file's extension.  Encoding
        # will be ignored, although we should check for simple things like
        # gzip'd or compressed files.
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            fp = open(path)
            # Note: we should handle calculating the charset
            msg = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'image':
            fp = open(path, 'rb')
            msg = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'audio':
            fp = open(path, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(path, 'rb')
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(fp.read())
            fp.close()
            # Encode the payload using Base64
            encoders.encode_base64(msg)
        # Set the filename parameter
        msg.add_header('Content-Disposition', 'attachment', filename=filename)

        outer_msg.attach(msg)
        return outer_msg

    def test_login(self):  # this will help to test email configurations
        server = None
        if self.is_smtp_ssl():
            server = smtplib.SMTP_SSL(host=self.smtp_server_address,
                                      port=self.smtp_port,
                                      timeout=self.timeout)
        else:
            server = smtplib.SMTP(host=self.smtp_server_address,
                                  port=self.smtp_port,
                                  timeout=self.timeout)
        server.set_debuglevel(1)
        # identify to server myself
        server.ehlo()
        if self.is_smtp_starttls():
            server.starttls()
            server.ehlo()

        #login server
        server.login(self.smtp_user_account, self.smtp_user_passwd)
        server.quit()
        return True

    def _send_mail(self,
                   toaddr,
                   msg):
        # send email
        server = None
        if self.is_smtp_ssl():
            server = smtplib.SMTP_SSL(host=self.smtp_server_address,
                                      port=self.smtp_port,
                                      timeout=self.timeout)
        else:
            server = smtplib.SMTP(host=self.smtp_server_address,
                                  port=self.smtp_port,
                                  timeout=self.timeout)
        server.set_debuglevel(1)
        # identify to server myself
        server.ehlo()
        if self.is_smtp_starttls():
            server.starttls()
            server.ehlo()

        #login server
        server.login(self.smtp_user_account, self.smtp_user_passwd)
        server.sendmail(self.fromaddr, toaddr, msg.as_string())
        server.quit()
        return True

    def _add_attachemnts_to_msg(self, outer_msg, attachments = None):
        if attachments is None:
            return outer_msg

        if isinstance(attachments, list):
            for attach in attachments:
                outer_msg = self.add_attachment(outer_msg, attach)
        else:
            outer_msg = self.add_attachment(outer_msg, attachments)
        return outer_msg

    def send_email(self,
                   toaddr,
                   subject="Qlabs Email(DO NOT REPLY)",
                   body="This is a test email!",
                   format='plain',
                   attachments=None):
        '''
        send a plain/html text email with attachements
        '''
        outer_msg = self.build_outer_msg(toaddr, subject, body, format)
        outer_msg = self._add_attachemnts_to_msg(outer_msg, attachments)
        return self._send_mail(toaddr, outer_msg)
