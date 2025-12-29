class AuthError(Exception):
    pass

class InvalidCredentials(AuthError):
    pass

class InvalidToken(AuthError):
    pass
