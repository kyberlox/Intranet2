from bitrix24 import Bitrix24
import requests
#import asyncio

class B24:
    def __init__(self):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/2158/qunp7dwdrwwhsh1w/")



    def getUsers(self):
        result = self.bx24.callMethod('user.get')
        return result

    def getDeps(self):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/2158/wk7uewb9l4xjo0xc/")
        result = self.bx24.callMethod('department.get')
        return result

    def getInfoBlock(self, id):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/2158/no7abhbtokxxctlb/")
        result = self.bx24.callMethod(f'lists.element.get?IBLOCK_TYPE_ID=lists&IBLOCK_ID={id}')
        return result



    def get_file(self, id, inf_id):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/1/j6122m0ystded5ag/")
        result = self.bx24.callMethod(f'disk.attachedObject.get?ENTITY_ID={inf_id}&id={id}')
        return result

    def get_all_files(self, id):
        url = f'https://portal.emk.ru/pub/rest/d105d8c66fc049a96c58d2cc18ea171e98c7ba89a9afa6425f003e42b4d90991/getBfileById.php?id={id}'
        response = requests.get(url)
        result = response.json()
        return result



    # функции vcard
    def getUsersByUuid(self, uuid):
        filter = {
                "XML_ID" : uuid
        }
        result = self.bx24.callMethod('user.search', filter=filter)
        return result

    def getDepartByID(self, id):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/2158/wk7uewb9l4xjo0xc/")
        result = self.bx24.callMethod('department.get', ID=id)
        return result



    def get_picture_link(self, inf_id, art_id, picture_type, property):
        link = f"https://portal.emk.ru/company/lists/{inf_id}/file/0/{art_id}/{picture_type}/{property}/"

        return link

    '''
    def find(self, inf_id, art_id, property):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/2158/no7abhbtokxxctlb/")
        result = self.bx24.callMethod(f"lists.field.get?IBLOCK_TYPE_ID=lists&IBLOCK_ID={inf_id}&FIELD_ID={property}")
        return result
    '''

    #async def getUsers(self):
        #result = await self.bx24.callMethod('user.get')
        #return result

'''
    def getUserKeys(self):
        result = self.bx24.callMethod('user.get')
        Keys = []
        for usr_dt in result:
            for key in usr_dt.keys():
                if key not in Keys:
                    Keys.append(key)
        return Keys

    #функция выводит все возможные варианты значения параметра пользователя:
    def variant_key_user(self, key = "WORK_POSITION"):
        usrs = self.getUsers()
        i = 0
        variants = []
        for usr in usrs:
            if key in usr and (usr[key] != "") and  ('LAST_NAME' in usr and 'NAME' in usr and 'SECOND_NAME' in usr):
                val = usr[key]
                fio = f"{usr['LAST_NAME']} {usr['NAME']} {usr['SECOND_NAME']}"
                if val[-1:] == " ":
                    val = val[:-1]

                if not variants:
                    i += 1
                    print("###", i)
                    variants = [{
                        "Номер": i,
                        "Должность": val,
                        "ФИО сотрудников": [fio]
                    }]
                else:
                    need_add = True
                    for sotr in variants:
                        if sotr["Должность"] == val:
                            sotr["ФИО сотрудников"].append(fio)
                            need_add = False

                    if need_add:
                        i += 1
                        print(i, val)
                        sotr = {
                            "Номер": i,
                            "Должность": val,
                            "ФИО сотрудников": [fio]
                        }
                        variants.append(sotr)



        return variants
'''
