# from src.base.pSQL.objects.DepartmentModel import DepartmentModel

# dep = DepartmentModel(Id=456).find_dep_by_id()
# print(dep)

import smtplib

server_mail_host = "smtp.emk.ru:587"

def try_mail(login, password):
    server = smtplib.SMTP(server_mail_host)
    server.starttls()
    server.login(login, password)
    

    status = server.noop()[0]
    server.quit()
    if status == 250:
        return True
    else:
        return False

# try_mail('kucherenko.m.d@emk.ru', "1234")
# try_mail('kucherenko.m.d@emk.ru', "1234")
try_mail("kucherenko.m.d@emk.ru", "RyfcfRF7vG")