import time

import requests
from cacheout import Cache
from requests import RequestException

from ys7_snap import settings
from ys7_snap.error import AccessTokenError, get_err_msg, CaptureError

cache = Cache(maxsize=500, ttl=settings.YS_TOKEN_CACHE_TIME, timer=time.time, default=None)


def get_access_token() -> str:
    """获取access token"""
    access_token = cache.get("access_token", None)
    if access_token:
        return access_token

    try:
        ys_token_get_url = settings.YS_TOKEN_GET_URL
        ys_app_key = settings.YS_APP_KEY
        ys_app_secret = settings.YS_APP_SECRET
        post_data = {
            "appKey": ys_app_key,
            "appSecret": ys_app_secret
        }

        data = requests.post(ys_token_get_url, data=post_data).json()
        rsp_code = data.get("code", 200)
        if rsp_code == "200":
            access_token = data['data']['accessToken']
            cache.set("access_token", access_token)
            return access_token
        else:
            raise AccessTokenError(get_err_msg(rsp_code))
    except RequestException as ex:
        raise AccessTokenError("访问萤石云请求失败")


def capture(device_serial: str, channel_no: str):
    """设备抓拍图片"""
    try:
        access_token = get_access_token()
        ys_mirror_url = settings.YS_CAPTURE_URL
        post_data = {
            'accessToken': access_token,
            'deviceSerial': device_serial,
            'channelNo': channel_no
        }

        data = requests.post(ys_mirror_url, data=post_data).json()
        rsp_code = data.get("code", 200)
        if rsp_code == "200":
            pic_url = data["data"]["picUrl"]
            return pic_url
    except AccessTokenError as ex:
        raise ex
    except Exception as ex:
        raise CaptureError(ex)
