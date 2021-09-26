import json


class Config:
    def __init__(self):
        with open("./settings.json", "r") as json_file:
            json_data = json.load(json_file)

        self.api_key = json_data["api_key"]
        self.ai_id = json_data["ai_id"]
        self.bot_id = json_data["bot_id"]
        self.bot_password = json_data["bot_password"]
        self.database_name = json_data["database_name"]
        self.database_user = json_data["database_user"]
        self.database_host = json_data["database_host"]
        self.database_password = json_data["database_password"]
