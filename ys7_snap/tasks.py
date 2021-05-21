import logging

from ys7_snap import aps, settings
from ys7_snap.remote import mqtt_public
from ys7_snap.store import save_to_local
from ys7_snap.ys7 import capture

log = logging.getLogger("ys7_snap")


@aps.timer(interval_seconds=settings.YS_SNAP_TIME)
def on_capture():
    videos = settings.VIDEOS
    if not videos:
        return

    for item in videos:
        try:
            url = capture(item["deviceSerial"], item["channelNo"])
            d = save_to_local(item, url)
            mqtt_public(settings.MQTT_TOPIC_TIME_SNAP_OUT, d)
        except Exception as ex:
            log.error(ex)
        continue
