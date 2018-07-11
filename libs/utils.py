#!/user/bin/python
import inspect
import json
from dash.exceptions import PreventUpdate

def caller_info():
    frame = inspect.currentframe().f_back
    func = frame.f_code
    return "func:{} line:{}".format(func.co_name,frame.f_lineno)
# exceptions
class RespExcept(Exception):
    def __init__(self,
                 error_message,
                 http_code=400):
        self.http_code =http_code
        self.error_message = error_message
        self._debug = None
    def __str__(self):
        return self._debug

class NotFound(RespExcept):
    def __init__(self, message="Not found"):
       super(NotFound, self).__init__(message, 404)
       self._debug = caller_info()

class AlreadyExist(RespExcept):
    def __init__(self, message="Already Exist"):
       super(AlreadyExist, self).__init__(message, 404)
       self._debug = caller_info()

class Conflict(RespExcept):
    def __init__(self, message="There are some conflicts"):
       super(NotFound, self).__init__(message, 404)
       self._debug = caller_info()

class LoginExpireMsg(RespExcept):
    def __init__(self, message="Login expired, please login again!"):
       super(NotFound, self).__init__(message, 404)
       self._debug = caller_info()

class CodeNotMatch(RespExcept):
    def __init__(self, message="Activate code does not match!"):
       super(NotFound, self).__init__(message, 404)
       self._debug = caller_info()

# helper functions
def g_id(module_name, name):
    return "{}-{}".format(module_name, name)


def load_user_info_from_storage(user_info_str):
    return user_info_str

def get_user_jwt(user_info_str):
    user_info = load_user_info_from_storage(user_info_str)
    return user_info


def load_cart_info_from_storage(cart_info_str):
    try:
        cart_info = json.loads(cart_info_str)
    except:
        cart_info = {}
    if not isinstance(cart_info, dict):
        cart_info = {}
    return cart_info

def assert_button_clicks(clicks):
    if not clicks or clicks <= 0:
        raise PreventUpdate()

def assert_has_value(obj):
    if not obj:
        raise PreventUpdate()

