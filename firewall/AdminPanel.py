#from .LogsMaker import LogsMaker
from ..code.src.services.Auth import AuthService
import subprocess

def check_and_add(username, password, ip_adress):
    #проверяю валидность на логин и пароль
    Auth().check_admin_credentials(username, password)

    #проверяю ip адрес
    need_update_wirewall = add_ip(ip_adress)

    #перезапускаю правила
    if need_update_wirewall:
        pass
        #subprocess.call(['bash', './setup_firewall.sh'])


def add_ip(ip_adress):
    #собираю с список ip адреса
    with open("admin_ip.txt") as adm_ip_file:
        adm_ip = []
        for ip in adm_ip_file:
             adm_ip.append(ip.strip())
    print(ip_adress, adm_ip)
    if ip_adress in adm_ip:
        return False
    else:
        #записываю в конец
        with open("admin_ip.txt", 'a') as adm_ip_file:  
            adm_ip_file.write(ip_adress + '\n')
        return True