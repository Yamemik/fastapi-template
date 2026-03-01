from enum import Enum
from modules.auth.domain.permissions import Permission


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


ROLE_PERMISSIONS = {
    Role.USER: {
        Permission.USER_READ,
    },
    Role.ADMIN: {
        Permission.USER_READ,
        Permission.USER_WRITE,
        Permission.ADMIN_PANEL,
    },
}
