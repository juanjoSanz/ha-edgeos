from homeassistant.config_entries import ConfigEntry

from .password_manager import PasswordManager
from ..helpers.const import *
from ..models.config_data import ConfigData


class ConfigManager:
    data: ConfigData
    config_entry: ConfigEntry
    password_manager: PasswordManager

    def __init__(self, password_manager: PasswordManager):
        self.password_manager = password_manager

    def update(self, config_entry: ConfigEntry):
        data = config_entry.data
        options = config_entry.options

        result = ConfigData()

        result.host = data.get(CONF_HOST)
        result.name = data.get(CONF_NAME)
        result.username = data.get(CONF_USERNAME)
        result.password = data.get(CONF_PASSWORD)
        result.unit = data.get(CONF_UNIT)

        result.monitored_devices = options.get(CONF_MONITORED_DEVICES, [])
        result.monitored_interfaces = options.get(CONF_MONITORED_INTERFACES, [])
        result.device_trackers = options.get(CONF_TRACK_DEVICES, [])
        result.update_interval = options.get(CONF_UPDATE_INTERVAL, 1)

        if len(result.password) > 0:
            result.password_clear_text = self.password_manager.decrypt(result.password)

        self.config_entry = config_entry
        self.data = result

    @staticmethod
    def _get_config_data_item(key, options, data):
        data_result = data.get(key, "")

        result = options.get(key, data_result)

        return result
