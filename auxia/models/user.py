from auxia.schemas.usuario import UserIn
from auxia.models.base import CreateBaseModel

class UserModel(UserIn, CreateBaseModel):
    pass