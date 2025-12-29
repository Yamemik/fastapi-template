from modules.auth.domain.interfaces import AuthProvider


class KeycloakAuthProvider(AuthProvider):
    async def authenticate(self, data):
        # redirect / token exchange
        ...

    async def validate_token(self, token: str):
        # introspection
        ...
