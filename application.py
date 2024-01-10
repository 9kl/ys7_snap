import time

import aps
import mq
import tasks

app_loop = True


class Application(object):
    def __init__(self):
        self.app_loop = True

    def run(self):
        try:
            mq.start()
            aps.scheduler.start()
            tasks.init()

            while self.app_loop:
                time.sleep(2)

            self.shutdown()
        except Exception as ex:
            raise ex

    def shutdown(self):
        aps.scheduler.shutdown()
        self.app_loop = False
