import requests


class RemoteServer(object):
    def __init__(self, host):
        self.host = host
        self.register()

    def register(self):
        endpoint = f"{self.host}/server/setup/"
        print(f"Connecting to: {endpoint}")

        answer = requests.post(endpoint)
        print(answer.status_code)
        if answer.ok:

            print("THIS REQUEST WAS OK!")
            json_answer = answer.json()
            print(json_answer)
        else:
            print(answer.__dict__)
