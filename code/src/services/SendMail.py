import os
from dotenv import load_dotenv

import smtplib
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText 

from src.services.LogsMaker import LogsMaker

load_dotenv()

server_mail_host = os.getenv('mail_server')
server_mail_login = os.getenv('mail_login')
server_mail_pswd = os.getenv('mail_password')

class SendEmail:
    def __init__(self, sender: str = '', reciever: str = '', title_msg: str = '', file_url: str = '', html_content=''):
        self.sender = sender
        self.reciever = reciever
        self.title_msg = title_msg
        self.file_url = file_url
        self.html_content = html_content

    def send_sucsesfell(self):
        msg = MIMEMultipart()
        msg["From"] = server_mail_login
        msg["To"] = self.sender
        msg['Subject'] = 'Сервис поздравительных открыток'
        html_content = """
        <html>
            <body>
                <p>Здравствуйте!</p>
                <p>Ваше письмо доставлено до получателя.</p>
                <p>
                    <img src="cid:company_logo" alt="Логотип компании" width="200">
                </p>
                <p>С уважением,<br>Команда АО "НПО "ЭМК".</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(html_content, "html"))

        # Загружаем логотип и добавляем его как встроенное изображение
        with open("./src/services/mail_logo.png", "rb") as img_file:
            logo = MIMEImage(img_file.read())
            logo.add_header("Content-ID", "<company_logo>") 
            logo.add_header("Content-Disposition", "inline", filename="mail_logo.png")
            msg.attach(logo)

        server = smtplib.SMTP(server_mail_host)
        server.starttls()
        server.login(server_mail_login, server_mail_pswd)
        server.send_message(msg)
        server.quit()
        return {'status': True}

    def send_congratulations(self):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender
            msg["To"] = self.reciever
            msg['Subject'] = self.title_msg

            content = self.html_content['html_content']
            
            
            """
            html_content = '''
            <html>
                <body>
                    <p>Здравствуйте!</p>
                    <p>
                        <img src="cid:file_logo" alt="Будущая открытка">
                    </p>
                    <p>Это тестовое письмо с логотипом компании в подписи.</p>
                    <p>
                        <img src="cid:company_logo" alt="Логотип компании" width="200">
                    </p>
                    <p>С уважением,<br>Команда АО "НПО "ЭМК".</p>
                </body>
            </html>
            '''
            """
            
            msg.attach(MIMEText(content, "html"))

            with open(f'.{self.file_url}', "rb") as img_file: 
                logo = MIMEImage(img_file.read())
                logo.add_header("Content-ID", "<file_logo>")  
                logo.add_header("Content-Disposition", "inline", filename="mail_logo.png")
                msg.attach(logo)

            # Загружаем логотип и добавляем его как встроенное изображение
            with open("./src/services/mail_logo.png", "rb") as img_file: 
                logo = MIMEImage(img_file.read())
                logo.add_header("Content-ID", "<company_logo>")  
                logo.add_header("Content-Disposition", "inline", filename="mail_logo.png")
                msg.attach(logo)

           
            server = smtplib.SMTP(server_mail_host)
            server.starttls()
            server.login(server_mail_login, server_mail_pswd)
            server.send_message(msg)
            server.quit()
            self.send_sucsesfell()
            return {'status': True}
        except SMTPException as e:
            return LogsMaker().error_message(e)
