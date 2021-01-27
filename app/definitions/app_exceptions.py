from fastapi import Request, status
from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code = {self.status_code} - context = {self.context}"
        )


async def app_exception_handler(request: Request, exc: AppExceptionCase):
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"app_exception": exc.exception_case, "context": exc.context},
    )


class AppException(object):
    class CreateResource(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Resource Creation Failed
            """
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            AppExceptionCase.__init__(self, status_code, context)

    class ResourceExists(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Resource Exists
            """
            status_code = status.HTTP_400_BAD_REQUEST
            AppExceptionCase.__init__(self, status_code, context)

    class ResourceDoesNotExist(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Resource does not exist
            """
            status_code = status.HTTP_404_NOT_FOUND
            AppExceptionCase.__init__(self, status_code, context)

    class Unauthorized(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Unauthorized
            :param context: extra dictionary object to give the error more context
            """
            status_code = status.HTTP_401_UNAUTHORIZED
            AppExceptionCase.__init__(self, status_code, context)
