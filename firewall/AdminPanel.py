#from .LogsMaker import LogsMaker
#from .Auth import AuthService

def check_and_add(username, password, ip_adress):
    #проверяю валидность на логин и пароль
    Auth().check_admin_credentials(username, password)

    #проверяю ip адрес
    need_update_wirewall = add_ip(ip_adress)

    #перезапускаю правила
    #if need_update_wirewall:


def add_ip(ip_adress):
    #собираю с список ip адреса
    with open("admin_ip.txt") as adm_ip_file:
        for ip in adm_ip_file:
            adm_ip = ip
    print(ip_adress, adm_ip)
    if ip_adress in adm_ip:
        return False
    else:
        #записываю в конец
        with open("admin_ip.txt", 'a') as adm_ip_file:  
            adm_ip_file.write(ip_adress + '\n')
        return True

add_ip("217.65.222.242")

add_ip("1.1.1.1")