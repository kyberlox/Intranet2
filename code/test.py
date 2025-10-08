# Настройки Redis из .env
import os
from dotenv import load_dotenv
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE

load_dotenv()
redis_username = os.getenv("user")
redis_password = os.getenv("pswd")

# Настройки Active Directory из .env
self.ldap_server = os.getenv("LDAP_SERVER")
self.ldap_domain = os.getenv("LDAP_DOMAIN")

self.session_ttl = timedelta(minutes=240)

def check_ad_credentials(self, username: str, password: str) -> Optional[str]:
        """Проверка учетных данных в AD"""
        try:

            #доступ админа
            if username in os.getenv("user") and password == os.getenv("pswd"):
                return {'GUID': "c97f2043-7e8a-4b0f-9bf7-e6bfcf9fccb6"}

            server = Server(self.ldap_server, get_info=ALL)
            conn = Connection(
                server,
                user=f"{username}@{self.ldap_domain}",
                password=password,
                authentication="SIMPLE"
            )

            if not conn.bind():
                return None

            search_filter = f"(sAMAccountName={username})"
            search_base = f"dc=imp,dc=int"
            conn.search(
                search_base,
                search_filter,
                search_scope=SUBTREE,
                attributes=[
                    'cn',
                    'mail',
                    'displayName',
                    'sAMAccountName',
                    'objectGUID',
                    'objectSID',
                    'userPrincipalName',
                    'distinguishedName',
                    'uidNumber',
                    'employeeID',
                    'employeeNumber',
                ]
            )

            if len(conn.entries) > 0:
                user_entry = conn.entries[0]

                # Преобразуем objectGUID
                object_guid = user_entry.objectGUID.value
                user_uuid = str(object_guid)[1:-1]

                # Преобразуем objectSID
                object_sid = user_entry.objectSID.value
                user_sid = str(object_sid)

                user_details = {
                    'cn': user_entry.cn.value,
                    'mail': user_entry.mail.value,
                    'displayName': user_entry.displayName.value,
                    'sAMAccountName': user_entry.sAMAccountName.value,
                    'GUID': user_uuid,
                    'SID': user_sid,
                    'userPrincipalName': user_entry.userPrincipalName.value,
                    'distinguishedName': user_entry.distinguishedName.value,
                    'uidNumber': user_entry.uidNumber.value if 'uidNumber' in user_entry else None,
                    'employeeID': user_entry.employeeID.value if 'employeeID' in user_entry else None,
                    'employeeNumber': user_entry.employeeNumber.value if 'employeeNumber' in user_entry else None,
                }

            else:
                return {"err" : "Пользователь не найден"}

            if not conn.entries:
                return None

            return user_details #str(conn.entries[0].objectGUID.value)

print(check_ad_credentials("timofeev.a.a", "!"))