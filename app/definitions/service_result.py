import inspect
from loguru import logger
from .app_exceptions import *


class ServiceResult(object):
    def __init__(self, args):
        if isinstance(args, AppExceptionCase):
            self.success = False
            self.exception_case = args.exception_case
            self.status_code = args.status_code
        else:
            self.success = True
            self.exception_case = None
            self.status_code = None

        self.value = args

    def __str__(self):
        if self.success:
            return "[Success]"
        return f'[Exception] "{self.exception_case}"'

    def __repr__(self):
        if self.success:
            return "<ServiceResult Success>"
        else:
            return f"<ServiceResult AppException {self.exception_case}>"

    def __enter__(self):
        return self.value

    def __exit__(self, *kwargs):
        pass


def caller_info() -> str:
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"


def handle_result(result: ServiceResult):
    if not result.success:
        with result as exception:
            logger.error(f"{exception} | caller={caller_info()}")
            raise exception
    with result as result:
        return result
