#!/usr/bin/python
import os

def locale_d():
    return  os.path.abspath(os.path.dirname(__name__)) + "/locale"

import gettext
zh = gettext.translation("magic_defines", locale_d(), languages=["zh_cn"])
zh.install(True)

SECRET_KEY = 'Thisissupposedtobesecret!'
UPLOAD_FOLDER = 'filestore/'
JWT_SECRET_KEY = 'super-secret'  # Change this!
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_HOURS = 2
EMAIL_SALT = 'email-confirmation-salt'

MAX_IMG_TXT = 10
CLUB_NAME = "haoduoyu"
IMAGE_SIZE = 1200, 1200
MAJOR_IMG = "major"
DEF_EXT = ".jpg"

USER_STORAGE = "user_info"
CART_STORAGE = "cart_info"
DUMMY_ID = "dummy_id"


#  id string defines
EMAIL = "email"
PASSWD = "passwd"
PASSWD_CONFIRM = "passwd-confirm"
SNACK_BAR = "snackbar"
REDIRECT = "redirect"
SUBMIT = "submit"
LOGIN = "login"
LOGOUT = "logout"
REGISTER = "register"
HIDDEN_DIV = "hidden-div"
STORAGE_W = "storage-writer"
STORAGE_R = "storage-reader"
TIMER = "timer"
ROOT = "root"
PLACEHOLDER = "place-holder"
USER_ID = "user-id"
TEL = "tel"
EDIT = "edit"
CONFIRM = "confirm"
ACTIVATE = "activate"
STATUS = "status"
CART = "CART"
CHECKOUT = "checkout"
CONTINUE_SHOP = "continue-shopping"
STORAGE_R2 = "storage-reader-2"
TABLE = "table"
# constant string defines, need translation
S_INPUT_EMAIL = _("Please input email!")
S_INPUT_PWD = _("Please input password!")
S_INPUT_PWD_CONFIRM = _("Please input password!")
S_INPUT_PWD_NOT_MATCH = _("Password not match!")
S_USER_EXIST = _("User already exist!")
S_USER_NOT_EXIST = _("User does not exist!")

S_USER_ID = _("User ID")
S_TEL= _("Tel")
S_PWD= _("Password")
S_PWD_CONFIRM= _("Password Confirmed")
S_EMAIL = _("Email")
S_ACTIVATE=_("Activated")
S_EDIT = _("Edit")
S_CONFIRM = _("Confirm")
S_ACTIVATE = _("Activate")
S_INPUT_ACTIVATE_CODE = _("Input Activate Code")
S_ACTIVE_STATUS = _("Active Status")
S_ACTIVE_NO = _("Not Active")
S_ACTIVE_YES = _("Active")
S_LOGOUT = _("Logout")
S_CHECKOUT= _("Checkout")
S_CONTINUE_SHOP = _("Continue Shopping")





# wechat related
# one wechat service number should have exact one token, AES_KEY, APP_ID
# wechat token
TOKEN = '1234567890google.com'
AES_KEY = '1234567890'
APP_ID = 'wx3e9dba3130c08266'
APP_SECRET = '30ce30ee5f13d70c09215ab2b6211f63'
def get_host():
    return "http://35.198.210.78"



