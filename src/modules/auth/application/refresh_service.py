from modules.auth.domain.exceptions import InvalidToken


class RefreshService:
    def __init__(self, jwt_manager, refresh_repo, user_repo):
        self.jwt = jwt_manager
        self.refresh_repo = refresh_repo
        self.user_repo = user_repo

    async def refresh(self, refresh_token: str):
        payload = self.jwt.decode(refresh_token)
        jti = payload["jti"]
        user_id = int(payload["sub"])

        stored = await self.refresh_repo.get_by_jti(jti)
        if not stored or stored.revoked:
            raise InvalidToken()

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise InvalidToken()

        # revoke old refresh token
        await self.refresh_repo.revoke(jti)

        access = self.jwt.create_access_token(user_id)
        new_refresh, new_jti = self.jwt.create_refresh_token(user_id)

        await self.refresh_repo.create(
            user_id=user_id,
            jti=new_jti,
            expires_at=stored.expires_at,
        )

        return {"access_token": access, "refresh_token": new_refresh}

    async def logout(self, refresh_token: str):
        payload = self.jwt.decode(refresh_token)
        await self.refresh_repo.revoke(payload["jti"])

    async def logout_all(self, user_id: int):
        await self.refresh_repo.revoke_all_for_user(user_id)
