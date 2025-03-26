from src.B24 import B24



class Article:
    def __init__(self, id=0, section_id=0):
        self.id = id
        self.section_id = section_id

    def get_inf(self):
        return B24().getInfoBlock(self.section_id)

    def add(self, data):
        '''
        ! Добавить статью и стандартизировать данные
        '''
        self.id = int(data['ID'])
        if "PREVIEW_TEXT" in data:
            preview = data['PREVIEW_TEXT']
        else:
            preview = None

        if "CONTENT_TEXT" in data:
            content = data['CONTENT_TEXT']
        elif "TEXT" in data:
            content = data['TEXT']
        else:
            content = None

        #if

        indirect_data = dict()
        article = ArticleDB(
            id=self.id,
            section_id=self.section_id,
            name = data['NAME'],
            preview_text = preview,
            content_text = content,
            date_publiction = date_publiction,
            date_creation = date_creation,
            indirect_data = indirect_data
        )

    def uplod(self):
        '''
        ! Не повредить имеющиеся записи и структуру
        '''

        #сопоставить section_id из Интранета и IBLOCK_ID из B24
        #однозначно
        sec_inb = {
            13 : "149", # Наши люди
            16 : "122", # Видеоитервью
            32 : "132", # Новости организационного развития
            53 : "62", # Афиша
            55 : "56" # Благотворительные проекты
        }

        for i in sec_inb:
            # найти статьи раздела в таблице
            ars = db.query(ArticleDB).filter(ArticleDB.section_id == i).all()

            # запрос в B24
            self.section_id = sec_inb[i]
            inbs = self.get_inf()

            # если в таблице есть раздел
            if ars is not None and ars != []:
                # если есть статья не попавшая в таблицу - добавить
                for ar in inbs:
                    self.id = int("ID")
                    artcl = db.query(ArticleDB).filter(ArticleDB.section_id == self.id).first()
                    if artcl is None:
                        self.section_id = i
                        self.add(ar)
            # если в таблице нет раздела
            else:
                for ar in inbs:
                    self.section_id = i
                    self.add(ar)

        #с параметрами
        #один section_id - несколько IBLOCK_ID
        #несколько section_id - один IBLOCK_ID

        #самобытные блоки
        #переделки
        #полная статика
        #новые разделы

