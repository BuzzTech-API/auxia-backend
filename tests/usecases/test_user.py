
import pytest
from auxia.usecases.user import user_usecase
from auxia.schemas.usuario import UserIn

@pytest.mark.asyncio
async def test_create_user(user_in: UserIn):
    created_user = await user_usecase.create_user(user_in)

    assert created_user.usr_name == user_in.usr_name
    assert created_user.usr_email == user_in.usr_email
    # assert "id" in created_user


@pytest.mark.asyncio
async def test_get_user(user_in: UserIn):
    # Criando um usuário de teste:
    await user_usecase.create_user(user_in)

    # Buscando usuário
    fetched_user = await user_usecase.get_user(user_in.usr_email)

    assert fetched_user.usr_name == user_in.usr_name
    assert fetched_user.usr_email == user_in.usr_email
    # assert "id" in fetched_user
