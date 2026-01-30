from sqlalchemy.orm.attributes import flag_modified

import datetime

#from ..models.User import User
#from .ActiveUsersModel import ActiveUsersModel

from .App import select, func #get_db
# db_gen = get_db()
# database = next(db_gen)


from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Мерча")



class MerchStoreModel:
    def __init__(self, user_id: str = ''):
        self.user_id = user_id

    async def upload_user_sum(self, session, value: int):
        try:
            from ..models.Roots import Roots
            
            stmt = select(Roots).where(Roots.user_uuid == int(self.user_id))
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if user:
                if user.user_points:
                    user.user_points += value
                else:
                    user.user_points = value
                # await session.commit()
            else:
                stmt_max = select(func.max(Roots.id))
                result_max = await session.execute(stmt_max)
                max_id = result_max.scalar() or 0
                new_id = max_id + 1

                new_user_sum = Roots(
                    id=new_id,
                    user_uuid=int(self.user_id),
                    root_token={},
                    user_points=value
                )

                session.add(new_user_sum)
                # await session.commit()
                
            return LogsMaker().info_message(f"Вы успешно начислили баллы пользователю с id = {int(self.user_id)}")
            
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в upload_user_sum при начислении баллов пользователю с id = {int(self.user_id)}, значение: {value}: {e}")

    async def create_purchase(self, session, data: dict):
        """
        Создание покупки мерча
        data: {"art_id": int, "l": int, "m": int, "s": int, "xl": int, "xxl": int, "no_size": int}
        """
        try:
            from ..models.Article import Article
            from ..models.Roots import Roots
            from ..models.PeerHistory import PeerHistory

            missing_items = {}
            shop_cart = {}
            error_flag = False
            art_id = data.pop("art_id")
            total_count = 0

            # Получаем информацию о мерче
            stmt_merch = select(Article).where(Article.id == art_id)
            result_merch = await session.execute(stmt_merch)
            merch_info = result_merch.scalar_one_or_none()

            if not merch_info:
                return LogsMaker().error_message(f"Ошибка в create_purchase: мерч с art_id = {art_id} не найден для пользователя {self.user_id}")

            # Проверяем доступность размеров
            for size, request_value in data.items():
                if request_value == 0 or request_value is None:
                    continue
                
                available_value = merch_info.indirect_data.get(size, 0)
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
                # return LogsMaker().warning_message(f"Недостаточно средств у пользователя с id = {self.user_id} для покупки мерча art_id = {art_id}")
                return {"not_enough": missing_items}

            # Рассчитываем общую стоимость
            total_price = total_count * merch_info.indirect_data.get('price', 0)
            
            # Проверяем баланс пользователя
            stmt_user = select(Roots).where(Roots.user_uuid == self.user_id)
            result_user = await session.execute(stmt_user)
            user = result_user.scalar_one_or_none()

            if not user or user.user_points is None:
                return LogsMaker().warning_message(f"Недостаточно средств у пользователя с id = {self.user_id} для покупки мерча art_id = {art_id}")
            elif total_price > user.user_points:
                return LogsMaker().warning_message(f"Недостаточно средств у пользователя с id = {self.user_id} для покупки мерча art_id = {art_id}. Нужно: {total_price}, есть: {user.user_points}")

            # Выполняем покупку
            for size, request_value in shop_cart.items():
                merch_info.indirect_data[size] = merch_info.indirect_data[size] - request_value

            flag_modified(merch_info, 'indirect_data')

            
            # Обновляем баланс пользователя
            money_left = user.user_points - total_price
            user.user_points = money_left
            # Добавляем запись в историю
            merch_description = f"{merch_info.name}, Куплено {total_count} штук(а)"
            add_history = PeerHistory(
                user_uuid=self.user_id,
                merch_info=merch_description,
                merch_coast=total_price,
                info_type='merch',
                date_time=datetime.datetime.now()
            )
            session.add(add_history)
            await session.commit()

            # TODO: добавить отправку на почту заказа
            LogsMaker().info_message(f"Пользователь с id = {self.user_id} успешно приобрел мерч art_id = {art_id}, количество: {total_count}, стоимость: {total_price}")
            return merch_description
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в create_purchase при покупке мерча пользователем {self.user_id}, данные: {data}: {e}")

    async def buy_split(self, session, data: dict):
        """
        Создание покупки старого замка
        data: {"art_id": int, "user_points": int}
        """
        try:
            from ..models.Article import Article
            from ..models.Roots import Roots
            from ..models.PeerHistory import PeerHistory

            art_id = data.pop("art_id")

            # Получаем информацию о мерче
            stmt_merch = select(Article).where(Article.id == art_id)
            result_merch = await session.execute(stmt_merch)
            merch_info = result_merch.scalar_one_or_none()

            if not merch_info:
                return LogsMaker().error_message(f"Ошибка в create_purchase: мерч с art_id = {art_id} не найден для пользователя {self.user_id}")


            # Рассчитываем общую стоимость
            total_price = 0
            
            # Проверяем баланс пользователя
            stmt_user = select(Roots).where(Roots.user_uuid == self.user_id)
            result_user = await session.execute(stmt_user)
            user = result_user.scalar_one_or_none()

            if not user or user.user_points is None:
                return LogsMaker().warning_message(f"Недостаточно средств у пользователя с id = {self.user_id} для покупки мерча art_id = {art_id}")
            elif data["user_points"] > user.user_points:
                return LogsMaker().warning_message(f"Пользователя с id = {self.user_id} хочет потратить больше, чем имеет")

            # Выполняем покупку
            merch_info.indirect_data['no_size'] -= 1

            flag_modified(merch_info, 'indirect_data')

            # Обновляем баланс пользователя
            # money_left = user.user_points - data["user_points"]
            user.user_points -= data["user_points"]
            # Добавляем запись в историю
            merch_description = f"Пользователь частично купил {merch_info.name}"
            add_history = PeerHistory(
                user_uuid=self.user_id,
                merch_info=merch_description,
                merch_coast=data["user_points"],
                info_type='merch',
                date_time=datetime.datetime.now()
            )
            session.add(add_history)
            await session.commit()

            # TODO: добавить отправку на почту заказа
            LogsMaker().info_message(f"Пользователь с id = {self.user_id} успешно приобрел мерч art_id = {art_id}, стоимость: {total_price}")
            return merch_description
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в create_purchase при покупке мерча пользователем {self.user_id}, данные: {data}: {e}")