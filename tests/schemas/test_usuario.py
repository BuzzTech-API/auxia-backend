from uuid import UUID

from pydantic import ValidationError
import pytest
from auxia.schemas.usuario import UserIn
from tests.factories import usuario_data

def test_schemas_return_sucess():
    data = usuario_data()
    user = UserIn.model_validate(data)

    assert user.usr_name == "Astolfo"
    assert user.usr_email == "astolfo@gmail.com"
    assert user.usr_password == "123456"
    assert user.usr_is_adm == True



    