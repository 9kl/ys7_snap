import json

import paho.mqtt.publish as publish

from ys7_snap import settings


def mqtt_public(topic, data):
    json_str = json.dumps(data)
    publish.single(topic, json_str, qos=1,
                   hostname=settings.MQTT_BROKE_URL,
                   port=settings.MQTT_BROKE_PORT,
                   client_id=settings.MQTT_CLIENT_ID)
