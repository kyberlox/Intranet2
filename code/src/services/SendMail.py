import os
from dotenv import load_dotenv

import smtplib
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText 

from .LogsMaker import LogsMaker

load_dotenv()

server_mail_host = os.getenv('mail_server')
server_mail_login = os.getenv('mail_login')
server_mail_pswd = os.getenv('mail_password')

STORAGE_PATH = "./files_db"

class SendEmail:
    def __init__(self, data=None):
        # self.sender = data['sender']
        # self.reciever = data['reciever']
        # self.title = data['title']
        # self.file_url = data['file_url'] 
        # self.html_content = data['text']
        self.data = data

    def send_sucsesfell(self):
        msg = MIMEMultipart()
        msg["From"] = server_mail_login
        msg["To"] = self.data['sender']
        msg['Subject'] = 'Сервис поздравительных открыток'
        html_content = """
        <html>
            <body>
                <p>Здравствуйте!</p>
                <p>Ваше письмо доставлено до получателя.</p>
                <p>С уважением,<br>Команда АО "НПО "ЭМК".</p>
                <p>
                    <img src="cid:company_logo" alt="Логотип компании" width="200">
                </p>
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
            msg["From"] = self.data['sender']
            msg["To"] = self.data['reciever']
            if self.data['title'] != '':
                msg['Subject'] = self.data['title']

            content = self.data['text']#['html_content']
            
            
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
            # print(self.data, 'send-service')
            msg.attach(MIMEText(content, "html"))
            file_id = self.file_url.split('/') #/intranet/Intranet2/code/files_db
            self.file_url = file_id[-1]
            file_path = os.path.join(STORAGE_PATH, self.file_url)
            with open(file_path, "rb") as img_file: 
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

    def send_error(self):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.data['sender']
            msg["To"] = 'it.dpm@emk.ru'
            msg['Subject'] = "баг репорт/интранет"

            content = self.data['text']#['html_content']
            
            
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
            # file_id = self.file_url.split('/') #/intranet/Intranet2/code/files_db
            # self.file_url = file_id[-1]
            # file_path = os.path.join(STORAGE_PATH, self.file_url)
            # with open(file_path, "rb") as img_file: 
            #     logo = MIMEImage(img_file.read())
            #     logo.add_header("Content-ID", "<file_logo>")  
            #     logo.add_header("Content-Disposition", "inline", filename="mail_logo.png")
            #     msg.attach(logo)

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

    def send_to_new_wrokers(self):
        msg = MIMEMultipart()
        msg["From"] = server_mail_login
        msg["To"] = self.data['sender']
        msg['Subject'] = 'Приветственное письмо'
        html_content = """
        <html>
            <body>
                <p>Приветствуем тебя, наш новый коллега!</p>
                <p>Надеюсь тебе у нас понравится. Желаем тебе карьерных высот, бешенной работоспособности и 3 сникерса ежедневно!</p>
                <p>С уважением,<br>Команда АО "НПО "ЭМК".</p>
                <p>
                    <img src="cid:company_logo" alt="Логотип компании" width="200">
                </p>
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