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

class  VerificationCodeExpireException(Exception):
    def __init___(self, message):
        super(VerificationCodeExpireException , self).__init__(message)
        self.message = message

class  InvalidCateogoryException(Exception):
    def __init___(self, message):
        super(InvalidCateogoryException , self).__init__(message)
        self.message = message

class  InvalidOrderingIndexException(Exception):
    def __init___(self, message):
        super(InvalidOrderingIndexException , self).__init__(message)
        self.message = message