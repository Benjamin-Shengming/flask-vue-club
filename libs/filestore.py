#!/user/bin/python
import os
import base64
from mimetypes import guess_extension, guess_type
from PIL import Image
from io import BytesIO
from magic_defines import *
import coloredlogs, logging
import shutil

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

def root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def filestore_dir():
    return os.path.join(root_dir(), "assets/filestore")

def service_dir_root():
    return os.path.join(filestore_dir(), "services")

def service_dir(service_id):
    return os.path.join(service_dir_root(), service_id)

def get_service_img_link(service_id, img_id):
    if not get_service_img_path(service_id, img_id):
        return ""
    link = "/assets/filestore/services/" + service_id + "/" + str(img_id) + DEF_EXT
    logger.debug(link)
    return link

def get_service_img_link_alt(service_id):
    img_id = 0
    for img_id in range(0, 10):
        link = get_service_img_link(service_id, img_id)
        if link:
            logger.debug(link)
            return link
    link = get_service_img_link(service_id, MAJOR_IMG)
    logger.debug(link)
    return link

def make_service_txt_path(service_id, txt_index):
    p = os.path.join(service_dir(service_id), "{}.txt".format(txt_index))
    if not os.path.exists(os.path.dirname(p)):
        os.makedirs(os.path.dirname(p))
    return p

def make_service_img_path(service_id, img_index):
    p = os.path.join(service_dir(service_id), str(img_index)+DEF_EXT)
    if not os.path.exists(os.path.dirname(p)):
        os.makedirs(os.path.dirname(p))
    return p

def get_service_txt_path(service_id, txt_index):
    p = os.path.join(service_dir(service_id), "{}.txt".format(txt_index))
    if os.path.isfile(p):
        return p
    return None

def get_service_img_path(service_id, img_index):
    p = os.path.join(service_dir(service_id), str(img_index)+DEF_EXT)
    if os.path.isfile(p):
        return p
    return None


def save_service_img(service_id, img_index, base64_content):
    if not base64_content:
        return
    logger.debug(base64_content)
    try:
        content_type, content_string = base64_content.split(',')
    except Exception as e:
        logger.debug("save image failed!" + str(e))
        return
    if "image" not in  content_type:
        return

    data_tag, base64_tag = content_type.split(";")
    if "base64" not in base64_tag:
        return
    # adjust size
    im = Image.open(BytesIO(base64.b64decode(content_string)))
    im.thumbnail(IMAGE_SIZE)
    rgb_im = im.convert('RGB')
    p = make_service_img_path(service_id, img_index)
    # save to file
    rgb_im.save(p)

def save_service_txt(service_id, txt_index, txt_content):
    if not txt_content:
        return
    p = make_service_txt_path(service_id, txt_index)
    with open(p, 'w') as f:
        f.write(txt_content)


def get_service_img_content(service_id, img_index):
    '''
    return base64 content with tag
    '''
    p = get_service_img_path(service_id, img_index)
    if not p:
        return None
    _, ext = os.path.splitext(p)
    content_string = None
    with open(p, 'rb') as f:
        content_string = base64.b64decode(f.read())
    return "data:img/{};base64,{}".format(ext) + str(content_string)

def get_service_txt_content(service_id, txt_index):
    '''
    return string content
    '''
    p = get_service_txt_path(service_id, txt_index)
    if not p:
        return None
    with open(p, 'r') as f:
        return f.read()

def del_service(service_id):
    dir_path = os.path.join(service_dir(service_id))
    shutil.rmtree(dir_path, True)

def copy_service_to_order_detail(service_id, order_detail_id):
    # order is a special service
    service_p = service_dir(service_id)
    order_detail_p = service_dir(order_detail_id)
    shutil.copytree(service_p, order_detail_p)

if __name__ == "__main__":
    print(service_dir())
