import json
import os

CONFIG_FILE_NAME = "transControllerConfig.json"

class UserConfig:
    def __init__(self):
        self.uid = -1
        self.username = ""
        self.permission = 0
        self.config = {}

        self.token = ""
        self.api_endpoint = ""
        self.ignore_list = []
        self.load_config()

    def load_config(self):
        if os.path.isfile(CONFIG_FILE_NAME):
            with open(CONFIG_FILE_NAME, "r", encoding="utf8") as f:
                self.config = json.load(f)
            self.token = self.config.get("token", "")
            self.api_endpoint = self.config.pop("api_endpoint", "")
            self.ignore_list = self.config.get("ignore_list", [])

    def set_userinfo(self, uid: int, username: str, token: str, permission: int):
        self.uid = uid
        self.username = username
        self.token = token
        self.permission = permission
        self.save_config()

    def set_api_endpoint(self, data: str):
        self.api_endpoint = data
        self.save_config()

    def save_config(self):
        self.config["token"] = self.token
        self.config["api_endpoint"] = self.api_endpoint
        self.config["ignore_list"] = self.ignore_list
        with open(CONFIG_FILE_NAME, "w", encoding="utf8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)


user_config = UserConfig()

