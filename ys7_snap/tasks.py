import logging
import time

from ys7_snap import aps, settings
from ys7_snap.remote import mqtt_public
from ys7_snap.store import local_save
from ys7_snap.ys7 import capture

log = logging.getLogger("ys7_snap")


@aps.timer(interval_seconds=settings.YS_SNAP_TIME)
def on_capture():
    videos = settings.VIDEOS
    if not videos:
        return

    for item in videos:
        try:
            device_serial = item["deviceSerial"]
            url = capture(item["deviceSerial"], item["channelNo"])

            picture_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            dir_name = time.strftime("%Y%m%d", time.localtime(time.time()))
            file_name = f"{device_serial}_{picture_time}.jpg"
            local_save(url, settings.FILE_SAVE_DIR, dir_name, file_name)
            d = {
                'video': item,
                'dir_name': dir_name,
                'file_name': file_name
            }
            mqtt_public(settings.MQTT_TOPIC_TIME_SNAP_OUT, d)
        except Exception as ex:
            log.error(ex)
        continue
