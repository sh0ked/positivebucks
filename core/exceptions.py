

class AppException(Exception):
    pass


class UserCreationException(AppException):
    pass


class UserNotFoundException(AppException):
    pass


class OrderCreationException(AppException):
    pass


class StorageException(AppException):
    pass
