class MuxError(BaseException):
    pass


class MissingHandlerError(MuxError):
    pass


class UncallableMiddlewareError(MuxError):
    pass
