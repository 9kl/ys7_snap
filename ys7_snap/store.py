import os
import time
import typing

import requests
from PIL import Image

from ys7_snap import settings
from ys7_snap.error import FileStoreError


def save_to_local(video: typing.Dict, url: str):
    """
    保存到本地
    :param video: 视频信息
    :param url: 抓拍图像url
    :return:
    """
    device_serial = video["deviceSerial"]
    picture_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    dir_name = time.strftime("%Y%m%d", time.localtime(time.time()))
    file_name = f"{device_serial}_{picture_time}.jpg"

    download_file(url, settings.FILE_SAVE_DIR, dir_name, file_name)

    if settings.THUMBNAIL_COMPRESSION_RATIO > 1:
        thumbnail_file_name = f"thumbnail_{file_name}"
        create_thumbnail(settings.FILE_SAVE_DIR, dir_name, file_name, thumbnail_file_name,
                         settings.THUMBNAIL_COMPRESSION_RATIO)
        file_name = thumbnail_file_name
    d = {
        'video': video,
        'dir_name': dir_name,
        'file_name': file_name
    }
    return d


def download_file(url: str, root_dir: str, save_dir: str, file_name: str):
    """
    下载文件并保存
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


def create_thumbnail(root_dir: str, file_dir: str, file_name: str, thumbnail_file_name: str, compression_ratio: int):
    """
    创建缩略图
    :param root_dir: 根目录
    :param file_dir: 文件目录
    :param file_name: 文件名称
    :param thumbnail_file_name: 缩略图文件名称
    :param compression_ratio: 缩略图压缩率
    :return:
    """
    file_path = os.path.join(root_dir, file_dir, file_name)
    if not os.path.exists(file_path):
        raise FileStoreError(f"生成缩略图原文件{file_path}不存在。")

    thumbnail_file_path = os.path.join(root_dir, file_dir, thumbnail_file_name)
    im = Image.open(file_path)
    w, h = im.size
    im.thumbnail((w // compression_ratio, h // compression_ratio))
    im.save(thumbnail_file_path, 'jpeg')
