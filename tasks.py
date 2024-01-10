import logging
import time

import aps
import settings
from remote import mqtt_public
from store import save_to_local
from ys7 import get_device_info, preset_move, capture

log = logging.getLogger("hniot_connect_sl651")


@aps.corn(settings.SNAP_CRON_EXPR)
def on_capture():
    videos = settings.VIDEOS
    if not videos:
        return

    for item in videos:
        try:
            device_serial = item["deviceSerial"]
            channel_no = item['channelNo']
            preset_index = item['presetIndex']
            def_preset_index = item['defPresetIndex']

            _device_info = get_device_info(device_serial)
            if not _device_info or _device_info.get('status', 0) == 0:
                continue

            if preset_index:
                preset_no_arr = [int(i) for i in preset_index.split(',')]
                for preset_no in preset_no_arr:
                    move_status = preset_move(device_serial, channel_no, preset_no)
                    if move_status:
                        time.sleep(10)
                        url = capture(item["deviceSerial"], item["channelNo"])
                        d = save_to_local(item, url)
                        d.update({'preset_no': preset_no})

                        mqtt_public(settings.MQTT_TOPIC_TIME_SNAP_OUT, d)
                if def_preset_index:
                    def_preset_no = int(def_preset_index)
                    preset_move(device_serial, channel_no, def_preset_no)
            else:
                url = capture(item["deviceSerial"], item["channelNo"])
                d = save_to_local(item, url)
                mqtt_public(settings.MQTT_TOPIC_TIME_SNAP_OUT, d)
        except Exception as ex:
            log.error(ex)
        continue


def init():
    pass
