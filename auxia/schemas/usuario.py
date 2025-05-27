from datetime import datetime

from typing import Optional
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


class UserUpdate(BaseSchemaIn):
    usr_name: Optional[str] = Field(None, description="User name")
    usr_email: Optional[str] = Field(None, description="User email")
    usr_password: Optional[str] = Field(None, description="User password")
    usr_is_adm: Optional[bool] = Field(None, description="Is or not adm")
    usr_is_active: Optional[bool] = Field(None, description="User is Active")


class UserUpdateMe(BaseSchemaIn):
    usr_name: Optional[str] = Field(None, description="User name")
    usr_password: Optional[str] = Field(None, description="User password")

from datetime import datetime

from typing import Optional
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


class UserUpdate(BaseSchemaIn):
    usr_name: Optional[str] = Field(None, description="User name")
    usr_email: Optional[str] = Field(None, description="User email")
    usr_password: Optional[str] = Field(None, description="User password")
    usr_is_adm: Optional[bool] = Field(None, description="Is or not adm")
    usr_is_active: Optional[bool] = Field(None, description="User is Active")


class UserUpdateMe(BaseSchemaIn):
    usr_name: Optional[str] = Field(None, description="User name")
    usr_password: Optional[str] = Field(None, description="User password")


class PasswordReset(BaseSchemaIn):
    usr_email: str = Field(..., description="Email do usuário")
    new_password: str = Field(..., description="Nova senha do usuário")