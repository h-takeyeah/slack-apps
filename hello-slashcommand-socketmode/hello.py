import _thread
import datetime
import json
import os
from json.decoder import JSONDecodeError
from urllib import error as ure
from urllib import request

import websocket


def respond(*arg: tuple) -> None:
    if len(arg) == 2:
        d = {"text": f"{arg[1]} is not supported."}
    else:
        d = greet()
    req = request.Request(
        arg[0],
        json.dumps(d).encode("utf8"),
        {"Content-Type": "application/json"},
    )
    try:
        request.urlopen(req)
    except ure.HTTPError as e:
        print("HTTPError", e.code)
    except ure.URLError as e:
        print(e.reason)


def greet() -> dict:
    h = datetime.datetime.now().hour
    if h < 3 or h >= 17:
        return {
            # The response_type parameter in the JSON payload controls this visibility,
            # by default it is set to ephemeral.
            "text": "Good evening!",
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "*Good evening!* :city_sunset:"},
                }
            ],
        }
    elif h >= 3 and h < 10:
        return {
            "text": "Good morning!",
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "*Good morning!* :chicken:"},
                }
            ],
        }

    else:
        return {
            "text": "Hello!",
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "*Hello!* :wave:"},
                }
            ],
        }


def on_message(ws: websocket._app.WebSocketApp, message: str) -> None:
    print(message)
    loaded = json.loads(message)

    envelope_id: str = loaded.get("envelope_id", "")

    # ack unless envelope_id is empty
    if envelope_id:
        ws.send(json.dumps({"envelope_id": envelope_id}))

    # respond to only slash_commands
    if loaded.get("type") != "slash_commands":
        return

    payload: dict = loaded.get("payload", {})

    # make sure payload is not empty
    if not bool(payload):
        return

    cmd = payload.get("command")
    if cmd == "/hello":
        _thread.start_new_thread(respond, (payload.get("response_url", ""),))
    else:
        _thread.start_new_thread(respond, (payload.get("response_url", ""), cmd))


def on_error(ws, error) -> None:
    print(error)


def on_close(ws, close_status_code, close_msg) -> None:
    print("### closed ###")


def on_open(ws) -> None:
    print("### opened ###")


def main() -> None:
    websocket.enableTrace(True)  # verbose log

    # websocket url to receive events data from slack
    ws_url: str = ""

    h = {
        "Content-type": "application/json",
        "Authorization": f'Bearer {os.environ.get("SLACK_APP_TOKEN")}',
    }
    req = request.Request(
        "https://slack.com/api/apps.connections.open", headers=h, method="POST"
    )

    try:
        # do POST request to get websocket url
        with request.urlopen(req) as res:
            from http import client

            if isinstance(res, client.HTTPResponse):
                d = json.loads(res.read().decode())
                if d.get("ok"):
                    # set given websocket url to ws_url
                    ws_url = d.get("url", "")
            else:
                print("res was not an instance of HTTPResponse")
                return

    except ure.HTTPError as e:
        print("HTTPError", e.code)  # 401, 500, ...

    except ure.URLError as e:
        print(e.reason)

    except JSONDecodeError as e:
        print(e)

    # successfully got websocket url
    else:
        # open websocket connection
        ws = websocket.WebSocketApp(
            ws_url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
        )

        ws.run_forever()


if __name__ == "__main__":
    main()
