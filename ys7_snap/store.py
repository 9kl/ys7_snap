import os

import requests

from ys7_snap.error import FileStoreError


def local_save(url: str, root_dir: str, save_dir: str, file_name: str):
    """
    本地文件存储
    :param url: 文件url
    :param root_dir: 根目录
    :param save_dir: 保存目录
    :param file_name: 文件名
    :return:
    """
    file_path = ""
    try:
        resp = requests.get(url)
        dir_path = os.path.join(root_dir, save_dir)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_path = os.path.join(dir_path, file_name)
        with open(file_path, 'wb') as f:
            f.write(resp.content)
    except requests.RequestException as ex:
        raise FileStoreError(f"request url{url} error,{ex}")
    except IOError as ex:
        raise FileStoreError(f"save file{file_path} error,{ex}")
