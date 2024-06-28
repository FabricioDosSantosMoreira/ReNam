# TODO: Change implementation and add more exceptions

class BaseException(Exception):

    message: str = "BaseException"

    def __init__(self, *, message: str) -> None:
        self.message = message


class APIFetcherException(BaseException):

    message: str = "APIFetcherException"

    def __init__(self, *, message: str) -> None:
        super().__init__(message=message)

        self.message = f"\nAPIFetcherException - - -> {self.message}"
        print(self.message)

