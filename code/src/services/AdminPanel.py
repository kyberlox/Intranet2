from src.services.LogsMaker import LogsMaker
from src.services.Auth import LogsMaker

def check_and_add(username, password, ip_adress):
    #проверяю валидность на логин и пароль
    Auth().check_admin_credentials(username, password)

    #проверяю ip адрес
    need_update_wirewall = add_ip(ip_adress)

    #перезапускаю правила
    if need_update_wirewall:


def add_ip(ip_adress):
    #собираю с список ip адреса
    with open("../../../firewall/admin_ip.txt") as adm_ip_file:
        adm_ip = adm_ip_file.readlines()
    
    if ip_adress in adm_ip:
        return False
    else:
        #записываю в конец
        with open('file.txt', 'a') as adm_ip_file:  
            adm_ip_file.write(ip_adress + '\n')

        return True

add_ip("217.65.222.242")

add_ip("1.1.1.1")

