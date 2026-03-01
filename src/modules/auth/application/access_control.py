from modules.auth.domain.roles import ROLE_PERMISSIONS, Role


class AccessControlService:
    def has_role(self, user, *roles: Role) -> bool:
        return user["role"] in roles

    def has_permission(self, user, permission) -> bool:
        role = Role(user["role"])
        return permission in ROLE_PERMISSIONS.get(role, set())
