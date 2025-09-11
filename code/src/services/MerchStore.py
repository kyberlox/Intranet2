from pSQL import MerchStoreModel
from fastapi import APIRouter, Body, Request

store_router = APIRouter(prefix="/store", tags=["Магазин мерча"])

class MerchStore:
    def __init__(self):
        pass

    def upload_sum(self):
        return MerchStoreModel().upload_user_sum()
    

@store_router.put("/upload_sum")
def upload_sum():
    return MerchStore().upload_sum()