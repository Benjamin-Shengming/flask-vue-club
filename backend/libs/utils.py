#!/user/bin/python
import inspect

def caller_info():
    frame = inspect.currentframe().f_back
    func = frame.f_code
    return "func:{} line:{}".format(func.co_name,frame.f_lineno)

class RespExcept(Exception):
    def __init__(self,
                 error_message,
                 http_code=400):
        self.http_code =http_code
        self.error_message = error_message

class NotFound(RespExcept):
    def __init__(self, message="Not found"):
       super(NotFound, self).__init__(message, 404)

class AlreadyExist(RespExcept):
    def __init__(self, message="Already Exist"):
       super(AlreadyExist, self).__init__(message, 404)

class Conflict(RespExcept):
    def __init__(self, message="There are some conflicts"):
       super(NotFound, self).__init__(message, 404)
