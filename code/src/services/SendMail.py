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
        try:
            company = '«Капитал ЭМК»'
            msg = MIMEMultipart()
            msg["From"] = server_mail_login
            msg["To"] = self.data['sender']
            msg['Subject'] = 'Приветственное письмо'
            text_msg = f'<p>Дорогой(ая) коллега!</p>\
                        <p>Рады приветствовать Вас в команде ЭМК!</p>\
                        <p>Первые шаги в новой компании — всегда особенное время. Желаем лёгкой 
                        адаптации, интересных задач и поддержки от коллег. Пусть работа приносит не 
                        только результат, но и удовольствие.</p>\
                        <p>В знак приветствия на Ваш счёт {company} зачислены стартовые баллы. 
                        Загляните в каталог — выберите то, что сделает первый месяц в компании чуточку приятнее.</p>\
                        <p>Спасибо, что выбрали ЭМК!</p>\
                        <p>С уважением,<br>Команда {company}.</p>'
            html_content = f'''
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        margin: 0;
                        padding: 20px;
                        font-family: Arial, sans-serif;
                        background-color: #f9f9f9;
                        color: #333;
                        line-height: 1.5;
                    }}
                    
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #ffffff;
                        padding: 30px;
                        border: 1px solid #ddd;
                    }}
                    
                    .text {{
                        margin-bottom: 30px;
                        white-space: pre-line;
                    }}
                    
                    .postcard {{
                        text-align: center;
                        margin: 30px 0;
                    }}
                    
                    .postcard img {{
                        max-width: 100%;
                        height: auto;
                        border: 1px solid #eee;
                    }}
                    
                    .logo {{
                        text-align: center;
                        margin: 30px 0;
                    }}
                    
                    .logo img {{
                        width: 200px;
                        height: auto;
                    }}
                    
                    .signature {{
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #eee;
                        font-size: 14px;
                        color: #666;
                        white-space: pre-line;
                    }}
                    
                    @media (max-width: 600px) {{
                        body {{
                            padding: 10px;
                        }}
                        
                        .container {{
                            padding: 20px;
                        }}
                        
                        .logo img {{
                            width: 150px;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="text">
                        {text_msg}
                    </div>
                    
                    <div class="logo">
                        <img src="cid:company_logo" alt="Логотип компании">
                    </div>
                </div>
            </body>
            </html>
            '''
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
        except Exception as e:
            LogsMaker().warning_message(f"Ошибка отправки письма новичку: {e}")
            return {'status': False} 
    
    def send_active_purchase(self):
        try:
            company = 'АО "НПО "ЭМК"'
            msg = MIMEMultipart() 
            msg["From"] = self.data['sender']
            msg["To"] = server_mail_login
            msg['Subject'] = 'Покупка мерча'
            items = self.data['items']
            user_info = self.data['user_info']
            text_msg = f'<p>Запрос на покупку мерча!</p>\
                        <p>Пользователь: {user_info}. Хочет приобрести: {items}</p>\
                        <p>С уважением,<br>Команда {company}.</p>'
            html_content = f'''
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        margin: 0;
                        padding: 20px;
                        font-family: Arial, sans-serif;
                        background-color: #f9f9f9;
                        color: #333;
                        line-height: 1.5;
                    }}
                    
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #ffffff;
                        padding: 30px;
                        border: 1px solid #ddd;
                    }}
                    
                    .text {{
                        margin-bottom: 30px;
                        white-space: pre-line;
                    }}
                    
                    .postcard {{
                        text-align: center;
                        margin: 30px 0;
                    }}
                    
                    .postcard img {{
                        max-width: 100%;
                        height: auto;
                        border: 1px solid #eee;
                    }}
                    
                    .logo {{
                        text-align: center;
                        margin: 30px 0;
                    }}
                    
                    .logo img {{
                        width: 200px;
                        height: auto;
                    }}
                    
                    .signature {{
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #eee;
                        font-size: 14px;
                        color: #666;
                        white-space: pre-line;
                    }}
                    
                    @media (max-width: 600px) {{
                        body {{
                            padding: 10px;
                        }}
                        
                        .container {{
                            padding: 20px;
                        }}
                        
                        .logo img {{
                            width: 150px;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="text">
                        {text_msg}
                    </div>
                    
                    <div class="logo">
                        <img src="cid:company_logo" alt="Логотип компании">
                    </div>
                </div>
            </body>
            </html>
            '''
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
        except Exception as e:
            LogsMaker().warning_message(f"Ошибка отправки письма новичку: {e}")
            return {'status': False} 

    def send_to_birthday_notifications(self):
        try:
            company = '«Капитал ЭМК»'
            msg = MIMEMultipart()
            msg["From"] = server_mail_login
            msg["To"] = self.data['sender']
            msg['Subject'] = 'С днем рождения!'
            text_msg = f'<p>Дорогой(ая) коллега!</p>\
                        <p>С днём рождения! </p>\
                        <p>Пусть новый год жизни приносит вдохновение в работе, радость в мелочах и поводы 
                        для гордости. Желаем энергии для смелых решений, лёгкости в трудные дни и людей 
                        рядом, которые делают путь интереснее.</p>\
                        <p>В знак внимания мы зачислили на Ваш счёт в {company} подарочные баллы. 
                        Загляните в каталог — выберите то, что порадует именно вас.</p>\
                        <p>Спасибо, что вы с нами!</p>\
                        <p>С уважением,<br>Команда {company}.</p>'
            html_content = f'''
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        margin: 0;
                        padding: 20px;
                        font-family: Arial, sans-serif;
                        background-color: #f9f9f9;
                        color: #333;
                        line-height: 1.5;
                    }}
                    
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #ffffff;
                        padding: 30px;
                        border: 1px solid #ddd;
                    }}
                    
                    .text {{
                        margin-bottom: 30px;
                        white-space: pre-line;
                    }}
                    
                    .postcard {{
                        text-align: center;
                        margin: 30px 0;
                    }}
                    
                    .postcard img {{
                        max-width: 100%;
                        height: auto;
                        border: 1px solid #eee;
                    }}
                    
                    .logo {{
                        text-align: center;
                        margin: 30px 0;
                    }}
                    
                    .logo img {{
                        width: 200px;
                        height: auto;
                    }}
                    
                    .signature {{
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #eee;
                        font-size: 14px;
                        color: #666;
                        white-space: pre-line;
                    }}
                    
                    @media (max-width: 600px) {{
                        body {{
                            padding: 10px;
                        }}
                        
                        .container {{
                            padding: 20px;
                        }}
                        
                        .logo img {{
                            width: 150px;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="text">
                        {text_msg}
                    </div>
                    
                    <div class="logo">
                        <img src="cid:company_logo" alt="Логотип компании">
                    </div>
                </div>
            </body>
            </html>
            '''
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
        except Exception as e:
            LogsMaker().warning_message(f"Ошибка отправки письма новичку: {e}")
            return {'status': False} 
    
    def send_to_anniversary_in_company(self, year):
        try:
            company = '«Капитал ЭМК»'
            msg = MIMEMultipart()
            msg["From"] = server_mail_login
            msg["To"] = self.data['sender']
            msg['Subject'] = 'С годовщиной!'
            text_msg = f'<p>Дорогой(ая) коллега!</p>\
                        <p>Сегодня особенный день — ровно {year} лет/год(а) назад Вы присоединились к нашей 
                        команде. Спасибо, что остаётесь с нами!</p>\
                        <p>Желаем, чтобы работа продолжала приносить удовольствие, а каждый новый год в  
                        компании открывал интересные возможности.</p>\
                        <p>В знак благодарности за Ваш стаж на счёт {company} зачислены баллы. 
                        Выбирайте подарок по душе в корпоративном каталоге.</p>\
                        <p>С уважением,<br>Команда {company}.</p>'
            html_content = f'''
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        margin: 0;
                        padding: 20px;
                        font-family: Arial, sans-serif;
                        background-color: #f9f9f9;
                        color: #333;
                        line-height: 1.5;
                    }}
                    
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #ffffff;
                        padding: 30px;
                        border: 1px solid #ddd;
                    }}
                    
                    .text {{
                        margin-bottom: 30px;
                        white-space: pre-line;
                    }}
                    
                    .postcard {{
                        text-align: center;
                        margin: 30px 0;
                    }}
                    
                    .postcard img {{
                        max-width: 100%;
                        height: auto;
                        border: 1px solid #eee;
                    }}
                    
                    .logo {{
                        text-align: center;
                        margin: 30px 0;
                    }}
                    
                    .logo img {{
                        width: 200px;
                        height: auto;
                    }}
                    
                    .signature {{
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #eee;
                        font-size: 14px;
                        color: #666;
                        white-space: pre-line;
                    }}
                    
                    @media (max-width: 600px) {{
                        body {{
                            padding: 10px;
                        }}
                        
                        .container {{
                            padding: 20px;
                        }}
                        
                        .logo img {{
                            width: 150px;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="text">
                        {text_msg}
                    </div>
                    
                    <div class="logo">
                        <img src="cid:company_logo" alt="Логотип компании">
                    </div>
                </div>
            </body>
            </html>
            '''
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
        except Exception as e:
            LogsMaker().warning_message(f"Ошибка отправки письма новичку: {e}")
            return {'status': False} 
    
    def send_to_jubilee_in_company(self, year):
        try:
            company = '«Капитал ЭМК»'
            msg = MIMEMultipart()
            msg["From"] = server_mail_login
            msg["To"] = self.data['sender']
            msg['Subject'] = 'С юилеем!'
            text_msg = f'<p>Дорогой(ая) коллега!</p>\
                        <p>{year} лет — это не просто цифра. Это годы, наполненные Вашим вкладом, идеями 
                        и поддержкой команды. Спасибо, что Вы с нами все эти годы!</p>\
                        <p>Ценим вашу преданность и профессионализм. Пусть следующие годы принесут 
                        новые вызовы, рост и яркие достижения.</p>\
                        <p>В честь юбилея на Ваш счёт {company} зачислено особое вознаграждение. 
                        С этими баллами в каталоге найдётся достойный выбор!</p>\
                        <p>С благодарностью,<br>Команда {company}.</p>'
            html_content = f'''
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        margin: 0;
                        padding: 20px;
                        font-family: Arial, sans-serif;
                        background-color: #f9f9f9;
                        color: #333;
                        line-height: 1.5;
                    }}
                    
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #ffffff;
                        padding: 30px;
                        border: 1px solid #ddd;
                    }}
                    
                    .text {{
                        margin-bottom: 30px;
                        white-space: pre-line;
                    }}
                    
                    .postcard {{
                        text-align: center;
                        margin: 30px 0;
                    }}
                    
                    .postcard img {{
                        max-width: 100%;
                        height: auto;
                        border: 1px solid #eee;
                    }}
                    
                    .logo {{
                        text-align: center;
                        margin: 30px 0;
                    }}
                    
                    .logo img {{
                        width: 200px;
                        height: auto;
                    }}
                    
                    .signature {{
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #eee;
                        font-size: 14px;
                        color: #666;
                        white-space: pre-line;
                    }}
                    
                    @media (max-width: 600px) {{
                        body {{
                            padding: 10px;
                        }}
                        
                        .container {{
                            padding: 20px;
                        }}
                        
                        .logo img {{
                            width: 150px;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="text">
                        {text_msg}
                    </div>
                    
                    <div class="logo">
                        <img src="cid:company_logo" alt="Логотип компании">
                    </div>
                </div>
            </body>
            </html>
            '''
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
        except Exception as e:
            LogsMaker().warning_message(f"Ошибка отправки письма новичку: {e}")
            return {'status': False} 
    