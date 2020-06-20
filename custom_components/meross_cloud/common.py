import logging
from abc import ABC

from meross_iot.controller.device import BaseDevice

from custom_components.meross_cloud.version import MEROSS_CLOUD_VERSION

_LOGGER = logging.getLogger(__name__)

# Constants
DOMAIN = 'meross_cloud'
ATTR_CONFIG = "config"
MANAGER = 'manager'
CLOUD_HANDLER = 'cloud_handler'
MEROSS_MANAGER = "%s.%s" % (DOMAIN, MANAGER)
SENSORS = 'sensors'
HA_SWITCH = 'switch'
HA_LIGHT = 'light'
HA_SENSOR = 'sensor'
HA_COVER = 'cover'
HA_CLIMATE = 'climate'
HA_FAN = 'fan'
#MEROSS_PLATFORMS = (HA_LIGHT, HA_SWITCH, HA_COVER, HA_SENSOR, HA_CLIMATE, HA_FAN)
MEROSS_PLATFORMS = (HA_SWITCH, HA_LIGHT, HA_COVER, HA_SENSOR)
CONNECTION_TIMEOUT_THRESHOLD = 5
CONF_STORED_CREDS = 'stored_credentials'


RELAXED_SCAN_INTERVAL = 180.0
SENSOR_SCAN_INTERVAL = 30


def calculate_sensor_id(uuid: str, type: str, measurement_unit: str, channel: int = 0,):
    return "%s:%s:%s:%s:%d" % (HA_SENSOR, uuid, type, measurement_unit, channel)


def calculate_cover_id(uuid: str, channel: int):
    return "%s:%s:%d" % (HA_COVER, uuid, channel)


def calculate_switch_id(uuid: str, channel: int):
    return "%s:%s:%d" % (HA_SWITCH, uuid, channel)


def calculate_light_id(uuid: str, channel: int):
    return "%s:%s:%d" % (HA_LIGHT, uuid, channel)


def dismiss_notification(hass, notification_id):
    hass.async_create_task(
        hass.services.async_call(domain='persistent_notification', service='dismiss', service_data={
            'notification_id': "%s.%s" % (DOMAIN, notification_id)})
    )


def notify_error(hass, notification_id, title, message):
    hass.async_create_task(
        hass.services.async_call(domain='persistent_notification', service='create', service_data={
            'title': title,
            'message': message,
            'notification_id': "%s.%s" % (DOMAIN, notification_id)})
    )


def log_exception(message: str = None, logger: logging = None, device: BaseDevice = None):
    if logger is None:
        logger = logging.getLogger(__name__)

    if message is None:
        message = "An exception occurred"

    device_info = "<Unavailable>"
    if device is not None:
        device_info = f"\tName: {device.name}\n" \
                      f"\tUUID: {device.uuid}\n" \
                      f"\tType: {device.type}\n\t" \
                      f"HW Version: {device.hardware_version}\n" \
                      f"\tFW Version: {device.firmware_version}"

    formatted_message = f"Error occurred.\n" \
                        f"-------------------------------------\n" \
                        f"Component version: {MEROSS_CLOUD_VERSION}\n" \
                        f"Device info: \n" \
                        f"{device_info}\n" \
                        f"Error Message: \"{message}\""
    logger.exception(formatted_message)
