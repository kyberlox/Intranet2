import json


from .App import select, func # db,



from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Активностей")



class ActivitiesModel:
    def __init__(self, id: int = 0, name: str = '', coast: int = 0, need_valid: bool = False, active: bool = False, is_auto: bool = False, description: str = ''):

        self.id = id
        self.name = name
        self.coast = coast
        self.need_valid = need_valid
        self.active = active
        self.is_auto = is_auto
        self.description = description

        
        from ..models.Activities import Activities
        self.Activities = Activities

    async def find_all_activities(self, session):
        try:
            stmt = select(self.Activities).where(self.Activities.active == True)
            result = await session.execute(stmt)
            activities = result.scalars().all()
            return activities
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в find_all_activities при получении списка активностей: {e}")

    async def update_activity(self, session, roots: dict):
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                stmt = select(self.Activities).where(self.Activities.id == self.id)
                result = await session.execute(stmt)
                activity = result.scalar_one_or_none()

                if activity:
                    activity.name = self.name
                    activity.coast = self.coast
                    activity.need_valid = self.need_valid
                    activity.active = self.active
                    activity.is_auto = self.is_auto
                    activity.description = self.description
                    await session.commit()

                    return LogsMaker().info_message(f"Обновление активности id = {self.id}, name = '{self.name}' завершено успешно")
                else:
                    return LogsMaker().warning_message(f"Активности с id = {self.id} не существует!")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав для обновления активности")
                
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в update_activity при обновлении активности id = {self.id}, name = '{self.name}': {e}")

    async def delete_activity(self, session, roots: dict):
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                stmt = select(self.Activities).where(
                    self.Activities.id == int(self.id), 
                    self.Activities.active == True
                )
                result = await session.execute(stmt)
                existing_activity = result.scalar_one_or_none()
                
                if existing_activity:
                    # Удаляем кураторов активности
                    from .PeerUserModel import PeerUserModel
                    peer_user_model = PeerUserModel(activities_id=existing_activity.id)
                    await peer_user_model.delete_curators(session, roots)
                    
                    # Деактивируем активность
                    existing_activity.active = False
                    # await session.commit()
                    
                    return LogsMaker().info_message(f"Удаление активности id = {self.id}, name = '{existing_activity.name}' завершено успешно")
                else:
                    return LogsMaker().warning_message(f"Активности с id = {self.id} не существует или она не активна!")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав для удаления активности")
                
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в delete_activity при удалении активности id = {self.id}: {e}")

    async def new_activity(self, session, data: dict, roots: dict):
        try: 
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                # Получаем максимальный ID
                stmt_max = select(func.max(self.Activities.id))
                result_max = await session.execute(stmt_max)
                max_id = result_max.scalar() or 0
                new_id = max_id + 1
                
                # Создаем новую активность
                new_active = self.Activities(
                    id=new_id,
                    name=data['name'],
                    coast=data['coast'],
                    need_valid=data['need_valid'],
                    active=True,
                    is_auto=data['is_auto']
                )
                if 'description' in data:
                    new_active = self.Activities(
                        id=new_id,
                        name=data['name'],
                        coast=data['coast'],
                        need_valid=data['need_valid'],
                        active=True,
                        is_auto=data['is_auto'],
                        description=data['description']
                    )

                
                # Если активность не требует подтверждения, назначаем куратора
                if data['need_valid'] == True:
                    session.add(new_active)
                    await session.commit()
                    return LogsMaker().info_message(f"Создание активности '{data['name']}' с id = {new_id} завершено успешно")
                else:
                    uuid = data['uuid']
                    from .PeerUserModel import PeerUserModel
                    peer_user_model = PeerUserModel(activities_id=new_id, uuid=uuid)
                    curator_status = await peer_user_model.add_curator(session, roots)
                    
                    if curator_status:
                        session.add(new_active)
                        await session.commit()
                        LogsMaker().info_message(f"Пользователь с id = {uuid} назначен куратором активности '{data['name']}'")
                        return LogsMaker().info_message(f"Создание активности '{data['name']}' с id = {new_id} завершено успешно")
                    else:
                        return LogsMaker().warning_message(f"Активность '{data['name']}' не была создана из-за ошибки назначения куратора!")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав для создания активности")
                
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в new_activity при создании активности '{data.get('name', 'unknown')}': {e}")

    # Дополнительный метод для загрузки базовых активностей (если нужно)
    async def upload_base_activities(self, session):
        try:
            import json
            with open('./src/base/peer-data/base_activities.json', mode='r', encoding='UTF-8') as f:
                cur_activities = json.load(f)
            
            for activity in cur_activities:
                stmt = select(self.Activities).where(self.Activities.id == activity['id'])
                result = await session.execute(stmt)
                existing_activity = result.scalar_one_or_none()
                
                if existing_activity:
                    continue
                else:
                    new_activity = self.Activities(
                        id=activity['id'], 
                        name=activity['name'], 
                        coast=activity['coast'], 
                        need_valid=activity['need_valid']
                    )
                    session.add(new_activity)
            
            await session.commit()
            return {"status": True}
            
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в upload_base_activities при загрузке базовых активностей: {e}")

