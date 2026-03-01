from enum import Enum


class Permission(str, Enum):
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    ADMIN_PANEL = "admin:panel"
