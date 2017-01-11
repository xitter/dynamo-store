class NotFoundException(Exception):
    def __init__(self, message=None):
        super(NotFoundException, self).__init__(message)


class InvalidInputException(Exception):
    def __init__(self, message=None):
        super(InvalidInputException, self).__init__(message)
