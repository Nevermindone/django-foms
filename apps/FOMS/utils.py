import glob
import subprocess
import os
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def export_to_pdf(input_file, output_dir='pdf_dir'):

    # Convert input_file to absolute path
    # input_file = os.path.abspath(input_file)

    # Create a directory for storing the output files
    os.makedirs(output_dir, exist_ok=True)

    # Run LibreOffice to export each page as a separate PDF
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, input_file],
                   shell=False)


def get_file_extension(file_name):
    return os.path.splitext(file_name)[1]


def send_email(recipient, subject, body, attachment_path=None):
    smtp_server = 'smtp.yandex.ru'
    port = 587
    from_email = settings.EMAIL_USER
    password = settings.EMAIL_PASSWORD
    to_email = recipient

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    body = body
    msg.attach(MIMEText(body, 'plain'))
    if attachment_path:
        attachment = open(attachment_path, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % attachment_path)

        msg.attach(part)

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()


def remove_files(folder_path):
    files = glob.glob(f'{folder_path}/*')
    for f in files:
        os.remove(f)
    os.rmdir(folder_path)
