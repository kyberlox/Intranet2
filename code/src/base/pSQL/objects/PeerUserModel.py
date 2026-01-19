from datetime import datetime

from datetime import timedelta


from .App import flag_modified, select, func, update, and_ # db, 

from src.services.LogsMaker import LogsMaker


class PeerUserModel:
    def __init__(self, activities_id: int = 0, uuid: int = 0, id: int = 0):
        self.activities_id = activities_id
        self.uuid = uuid
        self.id = id
        
        from ..models.Roots import Roots
        self.Roots = Roots
        
        from ..models.ActiveUsers import ActiveUsers
        self.ActiveUsers = ActiveUsers
        
        from ..models.Activities import Activities
        self.Activities = Activities
        
        from ..models.User import User
        self.User = User
        
        from ..models.PeerHistory import PeerHistory
        self.PeerHistory = PeerHistory

    async def points_to_confirm(self, session, roots):
        try:
            if "PeerModer" in roots.keys() and roots["PeerModer"] == True or "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                stmt = select(self.ActiveUsers, self.Activities).join(
                    self.Activities, 
                    self.Activities.id == self.ActiveUsers.activities_id
                ).where(
                    self.ActiveUsers.activities_id == self.Activities.id,
                    self.ActiveUsers.valid == 0,
                    self.Activities.id == self.activities_id
                )
                
                result = await session.execute(stmt)
                res = result.all()
                
                confirm_list = []
                if res:
                    for activities in res:
                        data = {
                            "id": activities[0].id,
                            "name": activities[1].name,
                            "uuid_from": activities[0].uuid_from,
                            "uuid_to": activities[0].uuid_to,
                            "description": activities[0].description,
                            "date_time": activities[0].date_time,
                            "coast": activities[1].coast,
                            "need_valid": activities[1].need_valid
                        }
                        confirm_list.append(data)
                return confirm_list
            else:
                return LogsMaker().warning_message(f"Недостаточно прав для получения списка модерируемых активностей")
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в points_to_confirm при получении активностей для подтверждения activities_id = {self.activities_id}: {e}")

    async def do_valid(self, session, action_id: int, uuid_to: int, roots: dict):
        try:
            if "PeerModer" in roots.keys() and roots["PeerModer"] == True or "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                stmt = select(self.Activities).join(
                    self.ActiveUsers, 
                    self.Activities.id == self.ActiveUsers.activities_id
                ).where(self.ActiveUsers.id == action_id)
                
                result = await session.execute(stmt)
                active_info = result.scalar_one_or_none()
                
                if active_info and active_info.need_valid == True:
                    stmt_update = update(self.ActiveUsers).where(self.ActiveUsers.id == action_id).values(valid=1)
                    await session.execute(stmt_update)
                    
                    # Начисляем баллы пользователю
                    from .MerchStoreModel import MerchStoreModel
                    merch_model = MerchStoreModel(uuid_to)
                    await merch_model.upload_user_sum(session, active_info.coast)

                    stmt = select(self.ActiveUsers.description).where(self.ActiveUsers.id == action_id)
                    result = await session.execute(stmt)
                    description = result.scalar_one_or_none()

                    add_history = self.PeerHistory(
                        user_uuid=int(self.uuid),
                        user_to=int(uuid_to),
                        active_info=f"Одобрено назанчение баллов пользователю: {description}",
                        active_coast=active_info.coast,
                        active_id=action_id,
                        info_type='activity',
                        date_time=datetime.now()
                    )

                    session.add(add_history)
                    await session.commit()
                    return True
                else:
                    return LogsMaker().info_message(f"Активности с id = {action_id} не существует или не требует подтверждения")
            return False
            
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в do_valid при подтверждении активности action_id = {action_id} для пользователя uuid_to = {uuid_to}: {e}")

    async def do_not_valid(self, session, action_id: int, roots: dict):
        try:
            if "PeerModer" in roots.keys() and roots["PeerModer"] == True or "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                stmt = select(self.Activities).join(
                    self.ActiveUsers, 
                    self.Activities.id == self.ActiveUsers.activities_id
                ).where(self.ActiveUsers.id == action_id)
                
                result = await session.execute(stmt)
                active_info = result.scalar_one_or_none()
                
                if active_info and active_info.need_valid == True:
                    stmt_update = update(self.ActiveUsers).where(self.ActiveUsers.id == action_id).values(valid=2)
                    await session.execute(stmt_update)

                    stmt = select(self.ActiveUsers.description, self.ActiveUsers.uuid_to).where(self.ActiveUsers.id == action_id)
                    result = await session.execute(stmt)
                    ActiveUsers_info = result.first()
                    add_history = self.PeerHistory(
                        user_uuid=int(self.uuid),
                        user_to=int(ActiveUsers_info[1]),
                        active_info=f"Отказано в получении баллов пользователю: {ActiveUsers_info[0]}",
                        active_coast=active_info.coast,
                        active_id=action_id,
                        info_type='activity',
                        date_time=datetime.now()
                    )

                    session.add(add_history)
                    await session.commit()
                    return True
                else:
                    return LogsMaker().info_message(f"Активности с id = {action_id} не существует или не требует подтверждения")
            return False
            
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в do_not_valid при отклонении активности action_id = {action_id}: {e}")

    async def get_curators(self, session):
        try:
            result = []
            stmt = select(self.Roots).where(self.Roots.root_token.has_key("PeerCurator"))
            query_result = await session.execute(stmt)
            curators = query_result.scalars().all()
            
            for curator in curators:
                for active_id in curator.root_token['PeerCurator']:
                    stmt_activity = select(self.Activities.name).where(self.Activities.id == active_id)
                    result_activity = await session.execute(stmt_activity)
                    active_name = result_activity.scalar_one_or_none()
                    
                    stmt_user = select(self.User.name, self.User.second_name, self.User.last_name).where(self.User.id == curator.user_uuid)
                    result_user = await session.execute(stmt_user)
                    curator_fio = result_user.first()
                    
                    if curator_fio and active_name:
                        active_info = {
                            'curator_id': curator.user_uuid,
                            "curator_name": curator_fio.name,
                            "curator_second_name": curator_fio.second_name,
                            "curator_last_name": curator_fio.last_name,
                            'activity_id': active_id,
                            'activity_name': active_name
                        }
                        result.append(active_info)
            return result
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в get_curators при получении списка кураторов: {e}")

    async def add_curator(self, session, roots: dict):
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                stmt = select(self.Roots).where(self.Roots.user_uuid == int(self.uuid))
                result = await session.execute(stmt)
                existing_curator = result.scalar_one_or_none()
                
                if existing_curator:
                    if "PeerCurator" in existing_curator.root_token.keys() and self.activities_id in existing_curator.root_token['PeerCurator']:
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} уже является куратором активности {self.activities_id}")
                    elif "PeerCurator" in existing_curator.root_token.keys():
                        existing_curator.root_token["PeerCurator"].append(self.activities_id)
                        flag_modified(existing_curator, 'root_token')
                        await session.commit()
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} добавлен как куратор активности {self.activities_id}")
                    else:
                        existing_curator.root_token["PeerCurator"] = [self.activities_id]
                        flag_modified(existing_curator, 'root_token')
                        await session.commit()
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} добавлен как куратор активности {self.activities_id}")
                else:
                    stmt_max = select(func.max(self.Roots.id))
                    result_max = await session.execute(stmt_max)
                    max_id = result_max.scalar() or 0
                    new_id = max_id + 1

                    new_moder = self.Roots(
                        id=new_id,
                        user_uuid=int(self.uuid),
                        root_token={"PeerCurator": [self.activities_id]}
                    )

                    session.add(new_moder)
                    await session.commit()
                    return LogsMaker().info_message(f"Пользователь с id = {self.uuid} добавлен как куратор активности {self.activities_id}")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав для добавления куратора")
                
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в add_curator при добавлении куратора user_id = {self.uuid} для активности {self.activities_id}: {e}")

    async def delete_curators(self, session, roots: dict):
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                stmt_activity = select(self.Activities).where(self.Activities.id == self.activities_id)
                result_activity = await session.execute(stmt_activity)
                existing_activity = result_activity.scalar_one_or_none()
                
                if existing_activity:
                    stmt_users = select(self.Roots).where(
                        self.Roots.root_token['PeerCurator'].contains([self.activities_id])
                    )
                    result_users = await session.execute(stmt_users)
                    users_with_activity = result_users.scalars().all()
                    
                    for user in users_with_activity:
                        if 'PeerCurator' in user.root_token.keys() and self.activities_id in user.root_token['PeerCurator']:
                            user.root_token['PeerCurator'].remove(self.activities_id)
                            flag_modified(user, 'root_token')
                            # await session.commit()

                    return LogsMaker().info_message(f"У активности с id = {self.activities_id} больше нет кураторов")
                else:
                    return LogsMaker().info_message(f"Активности с id = {self.activities_id} не существует")
            else:

                return LogsMaker().warning_message(f"Недостаточно прав для удаления кураторов")
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в delete_curators при удалении кураторов из активности {self.activities_id}: {e}")

    async def delete_curator(self, session, roots: dict):
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                stmt_user = select(self.Roots).where(
                    self.Roots.user_uuid == self.uuid,
                    self.Roots.root_token['PeerCurator'].contains([self.activities_id])
                )
                result_user = await session.execute(stmt_user)
                user = result_user.scalar_one_or_none()
                
                if user:
                    user.root_token['PeerCurator'].remove(self.activities_id)
                    flag_modified(user, 'root_token')
                    # await session.commit()
                    return LogsMaker().info_message(f"Пользователь с id = {self.uuid} больше не является куратором активности {self.activities_id}")
                else:
                    return LogsMaker().info_message(f"Пользователь с id = {self.uuid} не курировал активность {self.activities_id}")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав для удаления куратора")
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в delete_curator при удалении куратора user_id = {self.uuid} из активности {self.activities_id}: {e}")

    async def send_points(self, session, data: dict, roots: dict):
        try:
            from .MerchStoreModel import MerchStoreModel
            
            uuid_from = int(roots['user_id'])
            uuid_to = int(data["uuid_to"])
            activities_id = int(data["activities_id"])
            description = data["description"]
            
            # Проверяем существование пользователя
            stmt_user = select(self.User).where(self.User.id == uuid_to, self.User.active == True)
            result_user = await session.execute(stmt_user)
            existing_user = result_user.scalar_one_or_none()
            
            if not existing_user:
                return LogsMaker().warning_message(f"Пользователя с id = {uuid_to} не существует")

            month_ago = datetime.now() - timedelta(days=30)
            
            # Проверяем количество лайков за месяц
            stmt_count = select(func.count(self.ActiveUsers.id)).where(
                self.ActiveUsers.uuid_from == uuid_from,
                self.ActiveUsers.activities_id == activities_id,
                self.ActiveUsers.date_time >= month_ago
            )
            result_count = await session.execute(stmt_count)
            likes_count = result_count.scalar()

            # Получаем активности, требующие подтверждения
            stmt_needs = select(self.Activities.id).where(self.Activities.need_valid == True)
            result_needs = await session.execute(stmt_needs)
            needs = result_needs.scalars().all()

            if activities_id in needs:
                likes_left = 5 - likes_count
                if likes_left < 0:
                    return LogsMaker().warning_message(f"У пользователя с id = {uuid_from} закончились баллы для активности {activities_id}")
                elif uuid_from == uuid_to:
                    return LogsMaker().warning_message(f"Пользователь с id = {uuid_from} пытается поставить баллы сам себе!")
                else:
                    stmt_max = select(func.max(self.ActiveUsers.id))
                    result_max = await session.execute(stmt_max)
                    max_id = result_max.scalar() or 0
                    new_id = max_id + 1
                    
                    new_action = self.ActiveUsers(
                        id=new_id,
                        uuid_from=uuid_from,
                        uuid_to=uuid_to,
                        description=description,
                        activities_id=activities_id,
                        valid=0,
                        date_time=datetime.now()
                    )

                    session.add(new_action)
                    await session.commit()
                    return LogsMaker().info_message(f"Активность успешно отправлена пользователю с id = {uuid_to}")
                    
            elif "PeerCurator" in roots.keys() or "PeerAdmin" in roots.keys():
                stmt_max = select(func.max(self.ActiveUsers.id))
                result_max = await session.execute(stmt_max)
                max_id = result_max.scalar() or 0
                new_id = max_id + 1
                
                new_action = self.ActiveUsers(
                    id=new_id,
                    uuid_from=uuid_from,
                    uuid_to=uuid_to,
                    description=description,
                    activities_id=activities_id,
                    valid=1,
                    date_time=datetime.now()
                )

                
                value = 0
                flag = False
                
                if activities_id in roots.get("PeerCurator", []):
                    session.add(new_action)
                    await session.commit()
                    
                    stmt_coast = select(self.Activities.coast).where(self.Activities.id == activities_id)
                    result_coast = await session.execute(stmt_coast)
                    value = result_coast.scalar()
                    
                    merch_model = MerchStoreModel(uuid_to)
                    await merch_model.upload_user_sum(session, value)
                    flag = True
                    
                elif roots.get("PeerAdmin") == True:
                    session.add(new_action)
                    await session.commit()
                    
                    stmt_coast = select(self.Activities.coast).where(self.Activities.id == activities_id)
                    result_coast = await session.execute(stmt_coast)
                    value = result_coast.scalar()
                    
                    merch_model = MerchStoreModel(uuid_to)
                    await merch_model.upload_user_sum(session, value)
                    flag = True

                if flag:
                    add_history = self.PeerHistory(
                        user_uuid=roots['user_id'],
                        user_to=uuid_to,
                        active_info=description,
                        active_coast=value,
                        active_id=new_id,
                        info_type='activity',
                        date_time=datetime.now()
                    )

                    session.add(add_history)
                    await session.commit()
                    return LogsMaker().info_message(f"Активность успешно отправлена пользователю с id = {uuid_to}")
                else:
                    return LogsMaker().warning_message(f"Недостаточно прав для отправки активности")
                    
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в send_points при отправке баллов от {roots.get('user_id')} к {data.get('uuid_to')} для активности {data.get('activities_id')}: {e}")

    async def get_admins_list(self, session, roots: dict):
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                result = []
                stmt = select(self.Roots).where(self.Roots.root_token.has_key("PeerAdmin"))
                result_query = await session.execute(stmt)
                admins = result_query.scalars().all()
                
                for admin in admins:
                    if admin.root_token["PeerAdmin"] == True:
                        stmt_user = select(self.User.name, self.User.second_name, self.User.last_name).where(self.User.id == admin.user_uuid)
                        result_user = await session.execute(stmt_user)
                        admin_fio = result_user.first()
                        
                        if admin_fio:
                            admin_info = {
                                "admin_id": admin.user_uuid,
                                "admin_name": admin_fio.name,
                                "admin_second_name": admin_fio.second_name,
                                "admin_last_name": admin_fio.last_name
                            }
                            result.append(admin_info)
                return result
            else:
                return LogsMaker().warning_message(f"Недостаточно прав для просмотра списка администраторов")
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в get_admins_list при получении списка администраторов: {e}")

    async def add_peer_admin(self, session, roots: dict):
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                stmt = select(self.Roots).where(self.Roots.user_uuid == self.uuid)
                result = await session.execute(stmt)
                existing_admin = result.scalar_one_or_none()
                
                if existing_admin:
                    if "PeerAdmin" in existing_admin.root_token.keys() and existing_admin.root_token["PeerAdmin"] == True:
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} уже является администратором")
                    else:
                        existing_admin.root_token["PeerAdmin"] = True
                        flag_modified(existing_admin, 'root_token')
                        await session.commit()
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} назначен администратором")
                else:
                    stmt_max = select(func.max(self.Roots.id))
                    result_max = await session.execute(stmt_max)
                    max_id = result_max.scalar() or 0
                    new_id = max_id + 1

                    new_admin = self.Roots(
                        id=new_id,
                        user_uuid=int(self.uuid),
                        root_token={"PeerAdmin": True}
                    )

                    session.add(new_admin)
                    await session.commit()
                    return LogsMaker().info_message(f"Пользователь с id = {self.uuid} назначен администратором")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав для назначения администратора")
                
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в add_peer_admin при назначении администратора user_id = {self.uuid}: {e}")

    async def delete_admin(self, session, roots: dict):
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                stmt = select(self.Roots).where(self.Roots.user_uuid == int(self.uuid))
                result = await session.execute(stmt)
                existing_admin = result.scalar_one_or_none()

                if existing_admin:
                    if "PeerAdmin" in existing_admin.root_token.keys() and existing_admin.root_token["PeerAdmin"] == True:
                        existing_admin.root_token["PeerAdmin"] = False
                        flag_modified(existing_admin, 'root_token')

                        await session.commit()
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} больше не администратор")
                return LogsMaker().info_message(f"Пользователь с id = {self.uuid} не был администратором")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав для удаления администратора")
                
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в delete_admin при удалении администратора user_id = {self.uuid}: {e}")

    async def add_peer_moder(self, session, roots: dict):
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                stmt = select(self.Roots).where(self.Roots.user_uuid == self.uuid)
                result = await session.execute(stmt)
                existing_moder = result.scalar_one_or_none()
                
                if existing_moder:
                    if "PeerModer" in existing_moder.root_token.keys() and existing_moder.root_token["PeerModer"] == True:
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} уже является модератором")
                    else:
                        existing_moder.root_token["PeerModer"] = True
                        flag_modified(existing_moder, 'root_token')
                        await session.commit()
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} назначен модератором")
                else:
                    stmt_max = select(func.max(self.Roots.id))
                    result_max = await session.execute(stmt_max)
                    max_id = result_max.scalar() or 0
                    new_id = max_id + 1

                    new_moder = self.Roots(
                        id=new_id,
                        user_uuid=int(self.uuid),
                        root_token={"PeerModer": True}
                    )

                    session.add(new_moder)
                    await session.commit()
                    return LogsMaker().info_message(f"Пользователь с id = {self.uuid} назначен модератором")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав для назначения модератора")
                
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в add_peer_moder при назначении модератора user_id = {self.uuid}: {e}")

    async def delete_peer_moder(self, session, roots: dict):
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                stmt = select(self.Roots).where(self.Roots.user_uuid == self.uuid)
                result = await session.execute(stmt)
                existing_moder = result.scalar_one_or_none()
                

                if existing_moder:
                    if "PeerModer" in existing_moder.root_token.keys() and existing_moder.root_token["PeerModer"] == True:
                        existing_moder.root_token["PeerModer"] = False
                        flag_modified(existing_moder, 'root_token')

                        await session.commit()
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} больше не модератор")
                return LogsMaker().info_message(f"Пользователь с id = {self.uuid} не был модератором")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав для удаления модератора")
                
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в delete_peer_moder при удалении модератора user_id = {self.uuid}: {e}")

    async def get_moders_list(self, session, roots: dict):
        try:
            if "PeerModer" in roots.keys() and roots["PeerModer"] == True or "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                result = []
                stmt = select(self.Roots).where(self.Roots.root_token.has_key("PeerModer"))
                result_query = await session.execute(stmt)
                moders = result_query.scalars().all()
                
                for moder in moders:
                    if moder.root_token["PeerModer"] == True:
                        stmt_user = select(self.User.name, self.User.second_name, self.User.last_name).where(self.User.id == moder.user_uuid)
                        result_user = await session.execute(stmt_user)
                        moder_fio = result_user.first()
                        
                        if moder_fio:
                            moder_info = {
                                "moder_id": moder.user_uuid,
                                "moder_name": moder_fio.name,
                                "moder_second_name": moder_fio.second_name,
                                "moder_last_name": moder_fio.last_name
                            }
                            result.append(moder_info)
                return result
            else:
                return LogsMaker().warning_message(f"Недостаточно прав для просмотра списка модераторов")
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в get_moders_list при получении списка модераторов: {e}")

    async def get_curators_history(self, session, roots: dict):
        try:
            if "PeerAdmin" in roots.keys() or "PeerCurator" in roots.keys():
                stmt_history = select(self.PeerHistory).where(
                    self.PeerHistory.user_uuid == int(roots['user_id']),
                    self.PeerHistory.info_type == 'activity'
                )
                result_history = await session.execute(stmt_history)
                user_history = result_history.scalars().all()
                activity_history = []
                for active in user_history:
                    stmt_user = select(self.User.name, self.User.second_name, self.User.last_name).where(self.User.id == active.user_to)
                    result_user = await session.execute(stmt_user)
                    user_info = result_user.first()
                    
                    user_fio = ""
                    if user_info:
                        user_fio = f"{user_info.last_name or ''} {user_info.name or ''} {user_info.second_name or ''}".strip()
                    
                    stmt_activity = select(self.Activities.name).join(
                        self.ActiveUsers, 
                        self.ActiveUsers.activities_id == self.Activities.id
                    ).where(self.ActiveUsers.id == active.active_id)
                    
                    result_activity = await session.execute(stmt_activity)
                    active_name = result_activity.scalar_one_or_none()
                    
                    info = {
                        "id": active.id,
                        "date_time": active.date_time,
                        "uuid_to": active.user_to,
                        "uuid_to_fio": user_fio,
                        "description": active.active_info,
                        "activity_name": active_name,
                        "coast": active.active_coast

                    }
                    activity_history.append(info)
                
                return activity_history
            else:
                return LogsMaker().warning_message(f"Недостаточно прав для просмотра истории кураторов")
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в get_curators_history при получении истории кураторов для пользователя {roots.get('user_id')}: {e}")

    async def return_points_to_user(self, session, note_id: int, user_uuid: int):
        try:
            stmt_points = select(self.PeerHistory.merch_coast).where(self.PeerHistory.id == note_id)
            result_points = await session.execute(stmt_points)
            points = result_points.scalar_one_or_none()
            
            if points:
                stmt_delete = select(self.PeerHistory).where(self.PeerHistory.id == note_id)
                result_delete = await session.execute(stmt_delete)
                history_record = result_delete.scalar_one_or_none()
                
                if history_record:
                    await session.delete(history_record)
                    
                    stmt_user = select(self.Roots).where(self.Roots.user_uuid == user_uuid)
                    result_user = await session.execute(stmt_user)
                    user_info = result_user.scalar_one_or_none()
                    
                    if user_info:
                        user_info.user_points = user_info.user_points + points
                        await session.commit()
                        return True
            
            return LogsMaker().error_message(f"Ошибка при возврате средств: запись с id = {note_id} не найдена")
            
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в return_points_to_user при возврате средств пользователю {user_uuid} за запись {note_id}: {e}")

    async def remove_user_points(self, session, action_id: int, roots: dict):
        try:
            if "PeerModer" in roots.keys() and roots["PeerModer"] == True or "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                stmt_activity = select(self.Activities).join(
                    self.ActiveUsers, 
                    self.Activities.id == self.ActiveUsers.activities_id
                ).where(self.ActiveUsers.id == action_id)
                
                result_activity = await session.execute(stmt_activity)
                active_info = result_activity.scalar_one_or_none()
                
                if active_info:
                    stmt_action = select(self.ActiveUsers).where(
                        self.ActiveUsers.id == action_id,
                        self.ActiveUsers.valid == 1
                    )
                    result_action = await session.execute(stmt_action)
                    action_info = result_action.scalar_one_or_none()
                    
                    if action_info:
                        stmt_update = update(self.ActiveUsers).where(self.ActiveUsers.id == action_id).values(valid=2)
                        await session.execute(stmt_update)
                        
                        stmt_user = select(self.Roots).where(self.Roots.user_uuid == self.uuid)
                        result_user = await session.execute(stmt_user)
                        user_info = result_user.scalar_one_or_none()
                        
                        if user_info:
                            user_info.user_points = user_info.user_points - active_info.coast
                            await session.commit()
                            return LogsMaker().info_message(f"У пользователя с id = {self.uuid} сняты баллы за активность {action_id}")
                        else:
                            return LogsMaker().info_message(f"Пользователь с id = {self.uuid} не найден")
                    else:
                        return LogsMaker().info_message(f"Активность с id = {action_id} не была валидирована, баллы нельзя снять")
                else:
                    return LogsMaker().info_message(f"Активность с id = {action_id} не найдена")
            return False
            
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в remove_user_points при снятии баллов у пользователя {self.uuid} за активность {action_id}: {e}")
