from pydantic import Field
from auxia.schemas.base import BaseSchemaIn


class UserBase(BaseSchemaIn):
    usr_name: str = Field(..., description="User name")
    usr_email: str = Field(..., description="User email")
    usr_password: str = Field(..., description="User password")
    usr_is_adm: bool = Field(..., description="Is or not adm")


class UserIn(UserBase, BaseSchemaIn):
    pass
