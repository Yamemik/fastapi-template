from enum import Enum


class AuthType(str, Enum):
    LOCAL = "local"
    KEYCLOAK = "keycloak"
    AUTH0 = "auth0"
    MOCK = "mock"