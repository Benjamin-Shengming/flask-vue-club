#!/user/bin/python
import inspect
import json
import datetime
import calendar
from dash.exceptions import PreventUpdate
import coloredlogs, logging
from collections import OrderedDict
from random import randint

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


def method_log(log_obj):
    def decorator(fn):
        def decorated(*args, **kwargs):
            log_obj.info("start: {} \n ".format(fn.__name__))
            result = fn(*args, **kwargs)
            log_obj.info("end: {} \n".format(fn.__name__))
            return result
        return decorated
    return decorator


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

class PasswordExpire(RespExcept):
    def __init__(self, message="your password expired!"):
       super(NotFound, self).__init__(message, 404)
       self._debug = caller_info()

class PasswordInvalid(RespExcept):
    def __init__(self, message="your password not correct!"):
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
        logger.debug("load str")
        logger.debug(cart_info_str)
        cart_info = json.loads(cart_info_str, object_pairs_hook=OrderedDict)
    except Exception as e:
        logger.debug(str(e))
        cart_info = OrderedDict()
    if not isinstance(cart_info, dict):
        cart_info = OrderedDict()
    cart  = OrderedDict()
    for k, v in cart_info.items():
        try:
            cart[k] = int(v)
        except Exception as e:
            logger.debug(str(e))
            continue
    return cart

def calc_cart_total_price(cart):
    total = 0
    for _, v in cart.items():
        total += v
    return total

def assert_button_clicks(clicks):
    if not clicks or clicks <= 0:
        raise PreventUpdate()

def assert_has_value(obj):
    if not obj:
        raise PreventUpdate()


TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
def local_time_day():
    c = datetime.datetime.now()
    new = c.replace(hour=0, minute=0, second=0)
    return new

#Converts local time to UTC time
def local_2_utc(l):
    local = l.strftime(TIME_FORMAT)
    timestamp =  str(time.mktime(datetime.datetime.strptime(local, TIME_FORMAT).timetuple()))[:-2]
    utc = datetime.datetime.utcfromtimestamp(int(timestamp))
    return utc


#Converts UTC time to local time
def utc_2_local(u):
    utc = u.strftime(TIME_FORMAT)
    timestamp =  calendar.timegm((datetime.datetime.strptime( utc, TIME_FORMAT)).timetuple())
    local = datetime.datetime.fromtimestamp(timestamp)
    return local

def is_tel(s):
    s_str = str(s)
    return len(s_str) >= 6 and s_str.isdigit()

def is_email(s):
    return "@" in s and len(s) >= 3


def random_digits(length):
    code = ""
    for i in range(0, length):
        code += str(randint(0, 9))
    return code

