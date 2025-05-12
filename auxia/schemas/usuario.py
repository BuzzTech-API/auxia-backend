from datetime import datetime

from pydantic import Field

from auxia.schemas.base import BaseSchemaIn


class UserBase(BaseSchemaIn):
    usr_name: str = Field(..., description="User name")
    usr_email: str = Field(..., description="User email")
    usr_is_adm: bool = Field(..., description="Is or not adm")
    usr_is_active: bool = Field(..., description="User is Active")


class UserIn(UserBase, BaseSchemaIn):
    usr_password: str = Field(..., description="User password")


class UserOut(UserBase, BaseSchemaIn):
    created_at: datetime = Field()
