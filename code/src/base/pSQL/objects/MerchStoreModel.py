from sqlalchemy.orm.attributes import flag_modified

#from ..models.User import User
#from .ActiveUsersModel import ActiveUsersModel



from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Мерча")



class MerchStoreModel:

    def __init__(self, user_id: str = ''):
        from .App import db
        self.session = db
        self.user_id = user_id

    def upload_user_sum(self, value):
        from ..models.Roots import Roots
        try:
            user = self.session.query(Roots).filter(Roots.user_uuid == int(self.user_id)).first()
            if user:
                if user.user_points:
                    user.user_points += value
                    self.session.commit()
                else:
                    user.user_points = value
                    self.session.commit()
            else:
                new_user_sum = Roots(
                    user_uuid=int(self.user_id),
                    root_token={},
                    user_points=value
                )
                self.session.add(new_user_sum)
                self.session.commit()
            return LogsMaker().info_message(f"Вы успешно начислили баллы пользователю с id = {int(self.user_id)} ")
        except Exception as e:
            self.session.rollback()
            return LogsMaker().error_message(f"Ошибка начисления баллов пользователю с id = {int(self.user_id)}: {e}")
        finally:
            self.session.close()
    
    def create_purchase(self, data): # {"art_id": int, "l": int, "m": int, "s": int, "xl": int, "xxl": int, "no_size": int}
        from ..models.Article import Article
        from ..models.Roots import Roots
        from ..models.PeerHistory import PeerHistory

        missing_items = {}
        shop_cart = {}
        error_flag = False
        art_id = data.pop("art_id")
        total_count = 0
        merch_info = self.session.query(Article).filter(Article.id == art_id).scalar()
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
        user = self.session.query(Roots).filter(Roots.user_uuid == self.user_id).scalar()
        if total_price > user.user_points:
            return LogsMaker().warning_message(f"Недостаточно средств у пользователя с id = {self.user_id}")
        
        try:
            for size, request_value in shop_cart.items():
                merch_info.indirect_data[size] = merch_info.indirect_data[size] - request_value

            flag_modified(merch_info, 'indirect_data')
            money_left = user.user_points - total_price
            user.user_points = money_left
            self.session.commit()
            # добавляем сохранение
            merch_info = merch_info.name + ", " + "Куплено " + str(total_count) + "  штук(а)"
            add_history = PeerHistory(
                        user_uuid=self.user_id,
                        merch_info=merch_info,
                        merch_coast=total_price,
                        info_type='merch',
                        date_time=datetime.now()
                    )
            self.session.add(add_history)
            self.session.commit()
            # сюда добавить отправку на почту заказа
            return LogsMaker().info_message(f"Вы успешно приобрели мерч")
        except Exception as e:
            self.session.rollback()
            return LogsMaker().error_message(f"Ошибка при покупке мерча у пользователя с id = {self.user_id}: {e}")
        finally:
            self.session.close()