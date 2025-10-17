from sqlalchemy.orm.attributes import flag_modified

import datetime

#from ..models.User import User
#from .ActiveUsersModel import ActiveUsersModel
from .App import get_db
db_gen = get_db()
database = next(db_gen)


from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Мерча")



class MerchStoreModel:

    def __init__(self, user_id: str = ''):
        # from .App import db
        # database = db
        self.user_id = user_id

    def upload_user_sum(self, value):
        from ..models.Roots import Roots
        try:
            user = database.query(Roots).filter(Roots.user_uuid == int(self.user_id)).first()
            if user:
                if user.user_points:
                    user.user_points += value
                    database.commit()
                else:
                    user.user_points = value
                    database.commit()
            else:
                new_user_sum = Roots(
                    user_uuid=int(self.user_id),
                    root_token={},
                    user_points=value
                )
                database.add(new_user_sum)
                database.commit()
            return LogsMaker().info_message(f"Вы успешно начислили баллы пользователю с id = {int(self.user_id)} ")
        except Exception as e:
            database.rollback()
            return LogsMaker().error_message(f"Ошибка начисления баллов пользователю с id = {int(self.user_id)}: {e}")
    
    def create_purchase(self, data): # {"art_id": int, "l": int, "m": int, "s": int, "xl": int, "xxl": int, "no_size": int}
        from ..models.Article import Article
        from ..models.Roots import Roots
        from ..models.PeerHistory import PeerHistory

        missing_items = {}
        shop_cart = {}
        error_flag = False
        art_id = data.pop("art_id")
        total_count = 0
        merch_info = database.query(Article).filter(Article.id == art_id).scalar()
        for size, request_value in data.items():
            if request_value == 0 or request_value is None:
                continue
            
            available_value = merch_info.indirect_data[size]
            if available_value == 0 or available_value is None:
                missing_items[size] = request_value
                error_flag = True

            elif request_value > available_value:
                diff = request_value - available_value
                missing_items[size] = diff
                error_flag = True
            
            else:
                total_count += request_value
                shop_cart[size] = request_value

        if error_flag:
            return {"not_enough": missing_items}

        total_price = total_count * merch_info.indirect_data['price']
        user = database.query(Roots).filter(Roots.user_uuid == self.user_id).scalar()
        if user.user_points is None:
            return LogsMaker().warning_message(f"Недостаточно средств у пользователя с id = {self.user_id}")
        elif total_price > user.user_points:
            return LogsMaker().warning_message(f"Недостаточно средств у пользователя с id = {self.user_id}")
        
        try:
            for size, request_value in shop_cart.items():
                merch_info.indirect_data[size] = merch_info.indirect_data[size] - request_value

            flag_modified(merch_info, 'indirect_data')
            money_left = user.user_points - total_price
            user.user_points = money_left
            # database.commit()
            # добавляем сохранение
            merch_info = merch_info.name + ", " + "Куплено " + str(total_count) + "  штук(а)"
            add_history = PeerHistory(
                        user_uuid=self.user_id,
                        merch_info=merch_info,
                        merch_coast=total_price,
                        info_type='merch',
                        date_time=datetime.datetime.now()
                        # date_time=datetime.now()
                    )
            database.add(add_history)
            database.commit()
            # сюда добавить отправку на почту заказа
            return LogsMaker().info_message(f"Вы успешно приобрели мерч")
        except Exception as e:
            database.rollback()
            return LogsMaker().error_message(f"Ошибка при покупке мерча у пользователя с id = {self.user_id}: {e}")

