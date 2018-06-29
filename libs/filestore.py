#!/user/bin/python
import os
import base64

def root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def filestore_dir():
    return os.path.join(root_dir(), "assets/filestore")

def service_dir_root():
    return os.path.join(filestore_dir(), "services")

def service_dir(service_id):
    return os.path.join(service_dir_root(), service_id)

def make_service_txt_path(service_id, txt_index):
    p = os.path.join(service_dir(service_id), "{}.txt".format(txt_index))
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p))
    return p

def make_service_img_path(service_id, img_index, ext):
    p = os.path.join(service_dir(service_id), "{}.{}".format(img_index, ext))
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p))
    return p

def get_service_txt_path(service_id, txt_index):
    p = os.path.join(service_dir(service_id), "{}.txt".format(txt_index))
    if os.path.isfile(p):
        return p
    return None

def get_service_img_path(service_id, img_index):
    folder = service_dir(service_id)
    for filename in os.listdir(folder):
        if str(img_index) in filename and 'txt' not in filename:
            return os.path.join(folder, filename)
    return None


def save_service_img(service_id, img_index, base64_content):
    if not base64_content:
        return
    content_type, content_string = base64_content.split(',')
    if "image" not in  content_type:
        return

    data_tag, base64_tag = content_type.split(";")
    if "base64" not in base64_tag:
        return
    _, ext = data_tag.split("/")
    p = make_service_img_path(service_id, img_index, ext)
    with open(p, 'wb') as f:
        f.write(base64.b64decode(content_string))

    # adjust size

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
        content_string = base64.b64decod(f.read())
    return "data:img/{};base64,".format(ext) + content_string

def get_service_txt_content(service_id, txt_index):
    '''
    return string content
    '''
    p = get_service_txt_path(service_id, txt_index)
    if not p:
        return None
    with open(p, 'r') as f:
        return f.read()


if __name__ == "__main__":
    print(service_dir())
