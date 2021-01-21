import requests


class RemoteServer(object):
    def __init__(self, host, machine_id):
        self.host = host
        self.machine_id = machine_id
        self.register()

    def register(self):
        endpoint = f"{self.host}/server/setup/"
        print(f"Connecting to: {endpoint}")
        data = {"machine_id": self.machine_id}
        print(data)

        answer = requests.post(endpoint, data=data)
        print(answer.status_code)
        if answer.ok:

            print("THIS REQUEST WAS OK!")
            json_answer = answer.json()
            print(json_answer)
            screen_public_key = json_answer["screen_public_key"]
            screen_endpoint = f"{self.host}/screen/setup/{screen_public_key}"
            print(f"Screen will be pointed to: {screen_endpoint}")
            # os.system(f"snap set chromium-mir-kiosk url='{screen_endpoint}'")
        else:
            print(answer.__dict__)
