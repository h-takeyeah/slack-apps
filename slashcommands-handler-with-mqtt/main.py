import json
from json.decoder import JSONDecodeError
from typing import Any, Dict, Tuple
from urllib import request, error as ue

import paho.mqtt.client as mqtt

beebotte_host = 'mqtt.beebotte.com' # MQTT Broker
beebotte_port = 8883 # MQTT over TLS
beebotte_ch_token = 'token_xxxxxxxxxxx' # Your Channel's token

def respond_to_slack_slashcommand(response_url: str) -> None:
    msg = {
        'text': 'testtest',
        #'response_type': 'ephemeral', # (ephemeral: default) when it is related to slash command
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': 'This is section text.:+1:'
                }
            },
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'mrkdwn',
                        'text': 'This is footer text.'
                    }
                ]
            }
        ]
    }
    try:
        req = request.Request(response_url, json.dumps(msg).encode('utf8'), { 'Content-Type': 'application/json' })
        # Respond to slack client
        with request.urlopen(req):
            pass
    except (ValueError, ue.HTTPError): # Invalid URL value, 4xx/5xx error status
        pass

def on_connect(mqttc: mqtt.Client, _user_data, _flags, rc: int) -> None:
    if rc != 0: # "rc" is connection result
        err = {
            # Copied from paho.mqtt client.py
            1: 'Connection refused - incorrect protocol version',
            2: 'Connection refused - invalid client identifier',
            3: 'Connection refused - server unavailable',
            4: 'Connection refused - bad username or password',
            5: 'Connection refused - not authorised'
        }
        print(err[rc])
        return

    print('connected')
    mqttc.subscribe('test/res', 0)

def on_subscribe(_mqttc: mqtt.Client, _user_data, _mid, granted_qos) -> None:
    print('subscribed')
    print(_mid)
    print(granted_qos)

def on_message(mqttc: mqtt.Client, _, msg: mqtt.MQTTMessage) -> None:
    try:
        received_msg = json.loads(msg.payload)
        response_url = received_msg['data']['response_url']
        respond_to_slack_slashcommand(response_url)
    except JSONDecodeError:
        pass

def run() -> None:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.username_pw_set(f'token:{beebotte_ch_token}')
    client.tls_set('mqtt.beebotte.com.pem')

    client.will_clear()
    client.connect(beebotte_host, beebotte_port)
    client.loop_forever()

if __name__ == '__main__':
    run()
