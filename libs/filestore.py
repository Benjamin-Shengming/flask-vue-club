#!/user/bin/python
import os
import base64
from PIL import Image
from io import BytesIO
import coloredlogs
import logging
import shutil
import datetime
from magic_defines import (DEF_EXT, IMAGE_SIZE, MAJOR_IMG)
from utils import method_log
'''
service file name rule:
    year_month_day_hour_minute_second_microsecond-index.jpg
eg:
    2018_09_15_08_15_46_78695-0.jpg
'''
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


def datetime_to_str(dt):
    return "{}_{}_{}_{}_{}_{}_{}".format(dt.year,
                                         dt.month,
                                         dt.day,
                                         dt.hour,
                                         dt.minute,
                                         dt.second,
                                         dt.microsecond)


def root_dir():
    '''
    locate the root path of whole project
    '''
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def filestore_dir():
    return os.path.join(root_dir(), "assets/filestore")


def service_dir_root():
    return os.path.join(filestore_dir(), "services")


def service_dir(service_id):
    '''
    locate the one service folder
    '''
    return os.path.join(service_dir_root(), service_id)

@method_log(logger)
def get_service_img_link(service_id, img_id):
    file_path = get_service_img_path(service_id, img_id)
    if not file_path:
        return ""
    file_name = _get_filename(service_id, img_id, DEF_EXT)
    link = "/assets/filestore/services/" + service_id + "/" + str(file_name)
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


def _make_filename(index, ext):
    '''
    create a new file name based on index and ext
    '''
    dt = datetime.datetime.now()
    filename = None
    if ext.startswith("."):
        filename = "{}-{}{}".format(datetime_to_str(dt), str(index), ext)
    else:
        filename = "{}-{}.{}".format(datetime_to_str(dt), str(index), ext)
    return filename


def _get_filename(service_id, index, ext):
    expect_name = str(index) + ext if ext.startswith(".") else "." + ext
    service_d = service_dir(service_id)
    files = os.listdir(service_d)
    # scan all possible files
    potential_files = []
    for file_n in files:
        time_str, name_str = file_n.split(sep="-", maxsplit=1)
        if expect_name == name_str:
            potential_files.append(file_n)

    if not potential_files:  # no files found
        return None
    # only one file there
    if len(potential_files) == 1:
        return potential_files[0]
    # more than one file there, return the latest one
    # after sort, first item would be the latest one
    potential_files.sort(reverse=True)
    for old_item in potential_files[1:]:
        os.remove("{}/{}".format(service_d, old_item))
    return potential_files[0]


def _make_service_txt_path(service_id, txt_index):
    file_name = _make_filename(txt_index, ".txt")
    p = os.path.join(service_dir(service_id), file_name)
    if not os.path.exists(os.path.dirname(p)):
        os.makedirs(os.path.dirname(p))
    return p


def _make_service_img_path(service_id, img_index):
    file_name = _make_filename(img_index, DEF_EXT)
    p = os.path.join(service_dir(service_id), file_name)
    if not os.path.exists(os.path.dirname(p)):
        os.makedirs(os.path.dirname(p))
    return p


def get_service_txt_path(service_id, txt_index):
    file_name = _get_filename(service_id, txt_index, ".txt")
    if not file_name:
        return None
    p = os.path.join(service_dir(service_id), file_name)
    if os.path.isfile(p):
        return p
    return None


def get_service_img_path(service_id, img_index):
    file_name = _get_filename(service_id, img_index, DEF_EXT)
    if not file_name:
        return None
    p = os.path.join(service_dir(service_id), file_name)
    if os.path.isfile(p):
        return p
    return None


def save_service_img(service_id, img_index, base64_content):
    if not base64_content:
        return
    try:
        content_type, content_string = base64_content.split(',')
    except Exception as e:
        logger.debug("save image failed or not base64 " + str(e))
        return
    if "image" not in content_type:
        logger.debug("not image")
        return

    data_tag, base64_tag = content_type.split(";")
    if "base64" not in base64_tag:
        logger.debug("not base64")
        return
    # adjust size
    im = Image.open(BytesIO(base64.b64decode(content_string)))
    im.thumbnail(IMAGE_SIZE)
    rgb_im = im.convert('RGB')
    p = _make_service_img_path(service_id, img_index)
    # save to file
    rgb_im.save(p)


def save_service_txt(service_id, txt_index, txt_content):
    if not txt_content:
        return
    p = _make_service_txt_path(service_id, txt_index)
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
