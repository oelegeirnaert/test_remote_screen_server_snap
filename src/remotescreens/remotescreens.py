import requests
import logging

from remotescreens import machine_info

log = logging.getLogger(__name__)


class RemoteServer(object):
    def __init__(self, host):
        self.host = host
        self.machine_id = machine_info.get_machine_id()
        self.endpoint = f"{self.host}/server/api/"
        self.register()

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
        }
        answer = self.api_call(action="register", data=data)
        if answer:
            screen_public_key = answer.get("screen_public_key")
            if screen_public_key:
                screen_endpoint = f"{self.host}/screen/setup/{screen_public_key}"
                print(f"Screen will be pointed to: {screen_endpoint}")
                # os.system(f"snap set chromium-mir-kiosk url='{screen_endpoint}'")
