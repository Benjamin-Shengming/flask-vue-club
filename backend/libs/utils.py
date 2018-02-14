#!/user/bin/python
import inspect

def caller_info():
    frame = inspect.currentframe().f_back
    func = frame.f_code 
    return "func:{} line:{}".format(func.co_name,frame.f_lineno)

class RespExcept(Exception):
    def __init__(self, 
                 http_code, 
                 error_message):
        self.http_code =http_code 
        self.error_message = error_message

class NotFound(RespExcept):
    def __init__(self, message="Not found"):
       super(NotFound, self).__init__(404, message)

class Conflict(RespExcept):
    def __init__(self, message="There are some conflicts"):
       super(NotFound, self).__init__(404, message)
