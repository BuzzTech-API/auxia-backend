import pytest
from pydantic import ValidationError

from auxia.schemas.usuario import UserIn
from tests.factories import usuario_data


def test_user_schemas_return_sucess():
    data = usuario_data()
    user = UserIn.model_validate(data)

    assert user.usr_name == "Astolfo"
    assert user.usr_email == "astolfo@gmail.com"
    assert user.usr_password == "123456"
    assert user.usr_is_adm is True


def test_user_schemas_return_raise():
    data = {
        "usr_name": "Astolfo",
        "usr_email": "astolfo@gmail.com",
        "usr_is_adm": True,
    }

    with pytest.raises(ValidationError) as err:
        UserIn.model_validate(data)

        assert err.value.errors()[0] == {
            "type": "missing",
            "loc": ("usr_password",),
            "msg": "Field required",
            "input": data,
            "url": "https://errors.pydantic.dev/2.10/v/missing",
        }
