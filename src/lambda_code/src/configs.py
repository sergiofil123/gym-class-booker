import os
import json


class Configs:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configs, cls).__new__(cls)
            cls._instance._load_env_vars()
        return cls._instance

    def _load_env_vars(self):
        self.GYM_URL_API = os.getenv("GYM_URL_API", "")
        user_configs_var = os.getenv("USER_CONFIGS", "[]")
        gym_classes_configs_var = os.getenv("GYM_CLASSES_CONFIGS", "[]")

        try:
            self.USER_CONFIGS = json.loads(user_configs_var)
            self.GYM_CLASSES_CONFIGS = json.loads(gym_classes_configs_var)
        except json.JSONDecodeError as e:
            raise Exception(f"Error getting environment variables_ {e}")

    def get_user(self, name):
        for entry in self.USER_CONFIGS:
            if entry['name'] == name:
                return entry['email'], entry['password'], entry['user_id'], entry['user_center_id']
        return None, None, None, None

    def get_class_id(self, name):
        for entry in self.GYM_CLASSES_CONFIGS:
            if entry['name'] == name:
                return entry['id']
        return None
