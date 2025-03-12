from appium.options.android import UiAutomator2Options
from src.config import config


def get_capabilities(device_type: str) -> UiAutomator2Options:
    """
    Возвращает опции для подключения к Appium

    :param device_type: Тип устройства

    :return: UiAutomator2Options
    """
    options = UiAutomator2Options()
    options.automation_name = config.AUTOMATION_NAME
    options.platform_name = config.PLATFORM_NAME
    options.device_name = config.REAL_DEVICE_NAME
    options.app_package = config.APP_PACKAGE
    options.app_activity = config.APP_ACTIVITY
    options.new_command_timeout = config.NEW_COMMAND_TIMEOUT
    # options.waitForIdleTimeout = config.WAIT_FOR_IDLE_TIMEOUT
    # options.disableWindowAnimation = True
    # options.no_reset = True
    if device_type == "emulator":
        options.device_name = config.EMULATOR_DEVICE_NAME
        options.avd = config.EMULATOR_AVD

    return options
