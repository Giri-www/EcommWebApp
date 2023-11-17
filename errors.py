class MandatoryInputMissingException(Exception):
    def __init___(self, message):
        super(MandatoryInputMissingException, self).__init__(message)
        self.message = message

class InvalidMailPhoneException(Exception):
    def __init___(self, message):
        super(InvalidMailPhoneException, self).__init__(message)
        self.message = message

class CustomerExistsException(Exception):
    def __init___(self, message):
        super(CustomerExistsException, self).__init__(message)
        self.message = message