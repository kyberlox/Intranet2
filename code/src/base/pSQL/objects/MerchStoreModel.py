from sqlalchemy.orm.attributes import flag_modified

from ..models import User
from .App import db
from .ActiveUsersModel import ActiveUsersModel

from ....services.LogsMaker import LogsMaker

class MerchStoreModel:

    def __init__(self):
        self.session = db

    def upload_user_sum(self):
        users = self.session.query(User).filter(User.active == True).all()
        for user in users:
            user_sum = ActiveUsersModel(uuid_to=user.id).sum()
            user.indirect_data['user_points'] = user_sum
            flag_modified(user, 'indirect_data')
            self.session.commit()
        self.session.close()
        return True