# -*- coding: utf-8 -*-

import logging
import threading
import time

import paho.mqtt.client as mqtt

from ys7_snap import settings
from ys7_snap.remote import mqtt_public
from ys7_snap.ys7 import capture

log = logging.getLogger("ys7_snap")


def on_connect(client, userdata, flags, rc):
    # client.subscribe(settings.MQTT_TOPIC_REAL_SNAP_IN)
    client.subscribe('irr/photo/#')


def on_message(client, userdata, msg):
    if msg.topic == settings.MQTT_TOPIC_REAL_SNAP_IN:
        try:
            cmd = msg.payload.decode()
            if not settings.VIDEOS:
                return

            lst = [item for item in settings.VIDEOS if item['cmd'] == cmd]
            if lst:
                video = lst.pop()
                device_serial = video['deviceSerial']
                channel_no = video['channelNo']
                url = capture(device_serial, channel_no)
                d = {
                    "video": video,
                    "photo_url": url
                }
                mqtt_public(settings.MQTT_TOPIC_REAL_SNAP_OUT, d)
        except Exception as ex:
            log.error(ex)


client = mqtt.Client(client_id=settings.MQTT_CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message


def _create_mqtt_client():
    run = True
    while run:
        try:
            client.connect(settings.MQTT_BROKE_URL, settings.MQTT_BROKE_PORT, 60)
            client.loop_forever()
            run = False
        except Exception as ex:
            log.error(ex)
            run = True
            time.sleep(1)


def _thread_create_mqtt_client():
    t = threading.Thread(target=_create_mqtt_client)
    t.setDaemon(True)
    t.start()


def start():
    _thread_create_mqtt_client()


def shutdown():
    client.loop_stop()
