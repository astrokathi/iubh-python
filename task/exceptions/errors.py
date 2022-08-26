
class CustomError(Exception):
    """
    This is the Custom Base Exception
    """
    pass


class ObjectNoneError(CustomError):
    """
    This is the Custom Exception for Object None
    """
    def __init__(self, *args, **kwargs):
        pass
