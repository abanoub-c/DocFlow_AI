"""Base exceptions. main.py turns every AppError into one JSON error shape."""


class AppError(Exception):
    status_code: int = 500
    code: str = "internal_error"

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.code.replace("_", " ")
        super().__init__(self.message)


class NotFoundError(AppError):
    status_code = 404
    code = "not_found"


class ConflictError(AppError):
    status_code = 409
    code = "conflict"


class UnauthorizedError(AppError):
    status_code = 401
    code = "unauthorized"


class NotImplementedYet(AppError):
    """Placeholder for endpoints whose service layer is not built yet."""

    status_code = 501
    code = "not_implemented"