#!/user/bin/python
import requests
import coloredlogs, logging

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

class CebMobileMsg(object):
    def __init__(self):
        self.content_prefix = "【光大银行西安分行】"
        self.url = "http://wxapi.cebbanksrv.net/index.php/Msn/Index/index/.json"
        self.account = "106-xagd"

    def send(self, mobile_number, content):
       logger.debug("send message to " + mobile_number)
       url_encode_dict = {
           "account": self.account,
           "mobile": mobile_number,
           "content": self.content_prefix + content
       }
       r = requests.post(self.url, data=url_encode_dict)
       if int(r.text) == 1:
           logger.debug("send message succeed!")
           return True
       raise ValueError("send mobile message failed: {}".format(r.text))


if __name__ == "__main__":
    CebMobileMsg().send("13379506367", "好多鱼注册码测试 123456")



