import requests
import logging
import websocket
import time
import json
import subprocess
import datetime
from ast import literal_eval

from remotescreens import machine_info

try:
    import thread
except ImportError:
    import _thread as thread

log = logging.getLogger(__name__)


def on_message(ws, message):
    def send_error_message(ws, error_message, exception=None):
        print(error_message)
        print(str(exception))
        ws.send(
            json.dumps(
                {
                    "type": "command_result",
                    "message": {"error_message": error_message, "exception": str(exception)},
                }
            )
        )

    if message is None:
        return

    try:
        json_message = json.loads(message)
    except Exception as exc:
        send_error_message(ws=ws, error_message="Not a correct json format", exception=exc)
        return

    type = json_message.get("type", None)
    if type is None:
        send_error_message(ws=ws, error_message="cannot get a type from json")
        return

    if type.upper() == "SERVER_COMMAND":
        command = json_message.get("message", None)
        if command is None:
            send_error_message(ws=ws, error_message="cannot get a message from json")
            return

        try:
            command = literal_eval(command)
        except Exception as exc:
            send_error_message(ws=ws, error_message="cannot parse to array", exception=exc)
            return

        try:
            out = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = out.communicate()
            print(f"RESULT: {stdout}")
            print(f"ERROR: {stderr}")
            ws.send(
                json.dumps(
                    {"type": "command_result", "message": {"result": str(stdout), "error": str(stderr)}}
                )
            )
        except Exception as exc:
            send_error_message(ws=ws, error_message="cannot execute your command", exception=exc)


def on_error(ws, error):
    print("on_error")
    print(error)


def on_close(ws):
    print("connection closed...")
    wait_seconds = 5
    print(f"retrying in {wait_seconds} seconds.")
    time.sleep(wait_seconds)


def on_open(ws):
    print("Connection established")


class RemoteServer(object):
    def __init__(self, host):
        self.host = host
        self.machine_id = machine_info.get_machine_id()
        self.endpoint = f"{self.host}/server/api/"
        self.get_ws_endpoint()
        self.register()

    def get_ws_endpoint(self):
        self.ws_host = self.host.replace("http", "ws")
        if self.host.startswith("https"):
            self.ws_host = self.host.replace("https", "wss")

        print(self.ws_host)
        self.ws_endpoint = f"{self.ws_host}/ws/server/"
        print(self.ws_endpoint)

    def format_print(self):
        return "*" * 10

    def print_line(self):
        print("-" * 100)

    def print_info(self, message):
        print(
            f"""
    {self.format_print()} {message} {self.format_print()}
    Machine ID: {self.machine_id}
    Host: {self.host}
    """
        )

    def start_server(self):
        self.print_info("Starting Server...")

        if self.ws:

            def run(*args):
                while True:
                    time.sleep(30)
                    try:
                        self.ws.send(
                            json.dumps(
                                {
                                    "type": "server_status",
                                    "message": {"last_seen": str(datetime.datetime.now())},
                                }
                            )
                        )
                    except Exception as exc:
                        print(str(exc))

            thread.start_new_thread(run, ())

            while self.ws.run_forever():
                pass

    def status(self):
        self.print_info("Getting Status...")
        answer = self.api_call("status")

        if answer:
            server_public_key = answer.get("server_public_key")
            if server_public_key:
                self.print_info("PLEASE ACTIVATE THIS SERVER")

                self.print_line()
                url = f"{self.endpoint}?action=activate&server={server_public_key}"
                msg = "You can activate this server by clicking the following link:"
                print(msg.upper())
                print(url)
                self.print_line()

            if self.ws_connection_endpoint:
                ws = websocket.create_connection(self.ws_connection_endpoint)
                ws.send(
                    json.dumps(
                        {
                            "type": "server_status",
                            "message": {"last_seen": str(datetime.datetime.now()), "message": "Hello World!"},
                        }
                    )
                )
                ws.close()

    def api_call(self, action, data=None):
        post_data = {"machine_id": self.machine_id}
        if data:
            post_data["data"] = str(data)

        url = f"{self.endpoint}?action={action}"
        print(f"Connecting to: {url}")
        answer = requests.post(url, data=post_data)
        if answer.ok:
            print(answer.json())
            return answer.json()

        print(answer.__dict__)
        return None

    def register(self):
        self.print_info("Registering...")
        data = {
            "snap_info": machine_info.get_snap_info(),
            "platform_info": machine_info.get_platform_info(),
            "boot_time": machine_info.get_boot_time_info(),
            "network_info": machine_info.get_network_info(),
        }
        answer = self.api_call(action="register", data=data)
        if answer:
            screen_public_key = answer.get("screen_public_key")
            if screen_public_key:
                screen_endpoint = f"{self.host}/screen/setup/{screen_public_key}"
                print(f"Screen will be pointed to: {screen_endpoint}")
                # os.system(f"snap set chromium-mir-kiosk url='{screen_endpoint}'")

            self.websocket_id = answer.get("websocket_id")
            if self.websocket_id:
                self.ws_connection_endpoint = f"{self.ws_endpoint}{self.websocket_id}/"
                print(f"Websocket connection endpoint: {self.ws_connection_endpoint}")
                # websocket.enableTrace(True)
                self.ws = websocket.WebSocketApp(
                    self.ws_connection_endpoint,
                    on_message=on_message,
                    on_error=on_error,
                    on_close=on_close,
                )

                self.ws.on_open = on_open
