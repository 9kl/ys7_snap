import os
import uuid

import xlrd
from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def read_yml():
    with open(os.path.join(__location__, 'config.yml')) as f:
        data = load(f, Loader=Loader)
        return data


def read_videos_from_excel():
    """
    从excel中获取视频配置信息(deviceSerial, deviceName, channelNo, userData)
    :return:
    """
    file_path = os.path.join(__location__, 'videos.xls')
    book = xlrd.open_workbook(file_path)
    sh = book.sheet_by_index(0)
    lst = []
    for rx in range(sh.nrows):
        if rx == 0:
            continue

        item = {
            "deviceSerial": str(sh.cell_value(rx, 0)).strip(),
            "deviceName": sh.cell_value(rx, 1),
            "channelNo": int(sh.cell_value(rx, 2)),
            "presetIndex": str(sh.cell_value(rx, 3)).strip(),
            "defPresetIndex": str(sh.cell_value(rx, 4)).strip(),
            "cmd": str(sh.cell_value(rx, 5)),
            "userData": str(sh.cell_value(rx, 6))
        }
        lst.append(item)
    return lst


conf_data = read_yml()
VIDEOS = read_videos_from_excel()

if not conf_data.get('ys_app_key', None):
    raise RuntimeError('ys_app_key')

if not conf_data.get('ys_app_secret', None):
    raise RuntimeError('ys_app_secret')

if not conf_data.get('mqtt_broke_url', None):
    raise RuntimeError('mqtt_broke_url')

if not conf_data.get('mqtt_topic_time_snap_out', None):
    raise RuntimeError('mqtt_topic_time_snap_out')

if not conf_data.get('mqtt_topic_real_snap_in', None):
    raise RuntimeError('mqtt_topic_timing_snap_out')

if not conf_data.get('mqtt_topic_real_snap_out', None):
    raise RuntimeError('mqtt_topic_real_snap_out')

if not conf_data.get('ys_token_cache_time', None):
    raise RuntimeError('ys_token_cache_time')

if not conf_data.get('snap_cron_expr', None):
    raise RuntimeError('snap_cron_expr')

# 文件存储目录
FILE_SAVE_DIR = conf_data.get('file_save_dir', __location__)

# 图片缩略图参数
THUMBNAIL_COMPRESSION_RATIO = int(conf_data.get('thumbnail_compression_ratio', 1))

# mqtt
MQTT_BROKE_URL = conf_data.get('mqtt_broke_url')
MQTT_BROKE_PORT = int(conf_data.get('mqtt_broke_port', 1883))
MQTT_CLIENT_ID = conf_data.get('mqtt_client_id', str(uuid.uuid4()).replace('-', ''))
MQTT_TOPIC_TIME_SNAP_OUT = conf_data.get('mqtt_topic_time_snap_out')
MQTT_TOPIC_REAL_SNAP_IN = conf_data.get('mqtt_topic_real_snap_in')
MQTT_TOPIC_REAL_SNAP_OUT = conf_data.get('mqtt_topic_real_snap_out')

# ys7 config
YS_TOKEN_GET_URL = conf_data.get('ys_token_get_url', 'https://open.ys7.com/api/lapp/token/get')
YS_CAPTURE_URL = conf_data.get('ys_capture_url', 'https://open.ys7.com/api/lapp/device/capture')
YS_PRESET_MOVE_URL = conf_data.get('ys_preset_move_url', 'https://open.ys7.com/api/lapp/device/preset/move')
YS_DEVICE_INFO_URL = conf_data.get('ys_device_info_url', 'https://open.ys7.com/api/lapp/device/info')

YS_APP_KEY = conf_data.get('ys_app_key')
YS_APP_SECRET = conf_data.get('ys_app_secret')
YS_TOKEN_CACHE_TIME = conf_data.get('ys_token_cache_time')
# 抓拍定时器表达式
SNAP_CRON_EXPR = conf_data.get('snap_cron_expr')
