import logging.config
import signal
import time
from ys7_snap import tasks

from ys7_snap import aps, settings, mq

logging.config.dictConfig(settings.LOGGING_CONFIG)

log = logging.getLogger("hniot_connect_sl651")

app_loop = True


def start():
    try:
        mq.start()
        aps.scheduler.start()

        while app_loop:
            time.sleep(2)
    except Exception as ex:
        log.error(ex)


def stop(signum, frame):
    aps.scheduler.shutdown()
    mq.shutdown()

    global app_loop
    app_loop = False


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

if __name__ == '__main__':
    time.sleep(1)
    start()
