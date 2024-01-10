# -*- coding: utf-8 -*-

import logging.config
import signal

from application import Application

logging.config.fileConfig(fname="logger.conf", disable_existing_loggers=True)

app = Application()
app.run()

signal.signal(signal.SIGINT, app.shutdown())
signal.signal(signal.SIGTERM, app.shutdown())
