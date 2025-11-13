# # Настройки Redis из .env
# import os
# from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
# from typing import Optional, Dict, Any



# # Настройки Active Directory из .env
# ldap_server = os.getenv("LDAP_SERVER")
# ldap_domain = os.getenv("LDAP_DOMAIN")



# def check_ad_credentials(username: str, password: str) -> Optional[str]:
#         """Проверка учетных данных в AD"""

#         #доступ админа
#         if username in os.getenv("user") and password == os.getenv("pswd"):
#             return {'GUID': "c97f2043-7e8a-4b0f-9bf7-e6bfcf9fccb6"}

#         server = Server(ldap_server, get_info=ALL)
#         conn = Connection(
#             server,
#             user=f"{username}@{ldap_domain}",
#             password=password,
#             authentication="SIMPLE"
#         )

#         if not conn.bind():
#             return None

#         search_filter = f"(sAMAccountName={username})"
#         search_base = f"dc=imp,dc=int"
#         conn.search(
#             search_base,
#             search_filter,
#             search_scope=SUBTREE,
#             attributes=[
#                 'cn',
#                 'mail',
#                 'displayName',
#                 'sAMAccountName',
#                 'objectGUID',
#                 'objectSID',
#                 'userPrincipalName',
#                 'distinguishedName',
#                 'uidNumber',
#                 'employeeID',
#                 'employeeNumber',
#             ]
#         )

#         if len(conn.entries) > 0:
#             user_entry = conn.entries[0]

#             # Преобразуем objectGUID
#             object_guid = user_entry.objectGUID.value
#             user_uuid = str(object_guid)[1:-1]

#             # Преобразуем objectSID
#             object_sid = user_entry.objectSID.value
#             user_sid = str(object_sid)

#             user_details = {
#                 'cn': user_entry.cn.value,
#                 'mail': user_entry.mail.value,
#                 'displayName': user_entry.displayName.value,
#                 'sAMAccountName': user_entry.sAMAccountName.value,
#                 'GUID': user_uuid,
#                 'SID': user_sid,
#                 'userPrincipalName': user_entry.userPrincipalName.value,
#                 'distinguishedName': user_entry.distinguishedName.value,
#                 'uidNumber': user_entry.uidNumber.value if 'uidNumber' in user_entry else None,
#                 'employeeID': user_entry.employeeID.value if 'employeeID' in user_entry else None,
#                 'employeeNumber': user_entry.employeeNumber.value if 'employeeNumber' in user_entry else None,
#             }

#         else:
#             return {"err" : "Пользователь не найден"}

#         if not conn.entries:
#             return None

#             return user_details #str(conn.entries[0].objectGUID.value)

# print(check_ad_credentials("timofeev.a.a", "!"))
from src.base.pSQL.models.FilesDB import FilesDB
from src.base.pSQL.objects.App import select, func, AsyncSessionLocal
import asyncio


# async def test(art_id):
#     async with AsyncSessionLocal() as session:
#         stmt_max = select(FilesDB.name).where(
#             FilesDB.article_id == art_id
#         )
#         result_max = await session.execute(stmt_max)
#         all_names = result_max.scalars().all()
#         if all_names == []:
#             max_num = None
#         else:
#             nums = lambda x :  [int(n.split('_')[-1].split('.')[0]) for n in x ]
#             max_num = max(nums(all_names))

#         return max_num
        #return nums(all_names)
from bitrix24 import Bitrix24
def getInfoBlock(id):
    bx24 = Bitrix24("https://portal.emk.ru/rest/2158/no7abhbtokxxctlb/")
    result = bx24.callMethod(f'lists.element.get?IBLOCK_TYPE_ID=lists&IBLOCK_ID={id}')
    for res in result:
        if int(res['ID']) == 10855:
            return res
af = ["61", "83", "75", "77", "81", "82", "98", "78", "84"]
for sec in af:
    print(getInfoBlock(sec))