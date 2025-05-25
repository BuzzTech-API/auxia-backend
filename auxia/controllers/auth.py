from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Form
from fastapi.responses import JSONResponse
from auxia.models.auth import Token as TokenSchema
from auxia.usecases.auth import auth_usecase

router = APIRouter(prefix="/oauth", tags=["Auth"])

@router.post("/token", response_model=TokenSchema)
async def token_endpoint(
    grant_type: str = Form(..., alias="grant_type"),
    username: str | None = Form(None),
    password: str | None = Form(None),
    refresh_token: str | None = Form(None, alias="refresh_token"),
):
    # --- Password Grant ---
    if grant_type == "password":
        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "invalid_request",
                    "error_description": "Username e password são obrigatórios."
                }
            )

        user = await auth_usecase.authenticate_user(username, password)
        if not user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "invalid_grant",
                    "error_description": "Email ou senha inválidos."
                },
            )

        roles = ["me", "awnsers"] + (["users"] if user.usr_is_adm else [])
        expires_delta = timedelta(minutes=auth_usecase.ACCESS_TOKEN_EXPIRE_MINUTES)

        access = auth_usecase.create_access_token(
            subject=user.usr_email,
            roles=roles,
            expires_delta=expires_delta
        )
        refresh = await auth_usecase.create_refresh_token(user.usr_email)

        return TokenSchema(
            access_token=access,
            refresh_token=refresh,
            token_type="Bearer",
            expires_in=int(expires_delta.total_seconds()),
            scope=" ".join(roles),
        )

    # --- Refresh Grant ---
    if grant_type == "refresh_token":
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "invalid_request",
                    "error_description": "refresh_token é obrigatório."
                }
            )
        try:
            new_access, new_refresh, expires_in = await auth_usecase.refresh_access_token(refresh_token)
            return TokenSchema(
                access_token=new_access,
                refresh_token=new_refresh,
                token_type="Bearer",
                expires_in=expires_in,
                scope="",
            )
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content=e.detail)

    # --- Grant inválido ---
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "error": "unsupported_grant_type",
            "error_description": "Grant type não suportado."
        },
    )

@router.post("/revoke")
async def revoke_endpoint(
    refresh_token: str = Form(..., alias="refresh_token"),
):
    result = await auth_usecase.refresh_collection.update_one(
        {"tokenId": refresh_token},
        {"$set": {"revoked": True}}
    )
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token não encontrado ou já revogado."
        )
    return {"message": "Refresh token revogado com sucesso."}
