class AppError(Exception):

    def __init__(self, message: str, code: str = "APP_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class ConflictError(AppError):

    def __init__(self, message: str = "Resource already exists") -> None:
        super().__init__(message, "CONFLICT")


class UnauthorizedError(AppError):

    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message, "UNAUTHORIZED")


class ForbiddenError(AppError):

    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message, "FORBIDDEN")


class NotFoundError(AppError):

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, "NOT_FOUND")


class ExternalServiceError(AppError):

    def __init__(self, message: str = "External service error") -> None:
        super().__init__(message, "EXTERNAL_SERVICE_ERROR")
