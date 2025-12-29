from typing import Type

from modules.auth.domain.types.auth_type import AuthType

from ..domain.interfaces import AuthProvider
from ..infrastructure.providers.keycloak import KeycloakAuthProvider
from ..infrastructure.providers.local_jwt import LocalJWTAuthProvider
from ..infrastructure.providers.mock import MockAuthProvider


def get_auth_provider(auth_type: AuthType) -> Type[AuthProvider]:
    """
    Возвращает класс AuthProvider (не экземпляр).
    Экземпляр должен быть создан на уровне внедрения зависимостей (DI).
    """
    if auth_type == AuthType.LOCAL:
        return LocalJWTAuthProvider
    if auth_type == AuthType.KEYCLOAK:
        return KeycloakAuthProvider
    if auth_type == AuthType.MOCK:
        return MockAuthProvider

    raise ValueError("Unsupported auth type")
