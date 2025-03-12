import os
import pytest
import logging
from dotenv import load_dotenv
from appium import webdriver
from src.config.capabilities import get_capabilities
from src.helpers.logging import setup_logger
from src.helpers.screenshot import attach_screenshot


load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--device",
        action="store",
        default="emulator",
        help="Выбор устройства: 'emulator' (по умолчанию) или 'real'",
    )
    parser.addoption(
        "--server",
        action="store",
        default="LOCAL_APPIUM_SERVER",
        help="Выбор сервера: LOCAL_APPIUM_SERVER, REMOTE_APPIUM_SERVER",
    )
    parser.addoption(
        "--log_level",
        action="store",
        default="INFO",
        help="Уровень логирования (DEBUG, INFO, WARNING, ERROR)",
    )


@pytest.fixture(scope="session")
def device_type(request):
    """
    Фикстура возвращает тип устройства
    """
    return request.config.getoption("--device")


@pytest.fixture(scope="session")
def base_server(request):
    """
    Фикстура возвращает базовый сервер
    """
    return os.getenv(request.config.getoption("--server"))


@pytest.fixture(scope="session")
def logger():
    """
    Фикстура для логирования
    """
    return setup_logger()


@pytest.fixture()
def driver(request, base_server, logger, device_type):
    """
    Фикстура для инициализации драйвера
    :param request:
    :param base_server:
    :param logger:
    :param device_type:
    """
    log_level = request.config.getoption("--log_level")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    capabilities = get_capabilities(device_type)
    driver = webdriver.Remote(base_server, options=capabilities)
    driver.logger = logger
    logger.info(f"Драйвер запущен. Уровень логирования: {log_level.upper()}")

    yield driver
    if request.node.rep_call.failed:
        attach_screenshot(driver, request.node.name)

    driver.quit()
    logger.info(f"Драйвер закрыт. Уровень логирования: {log_level.upper()}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Хук pytest: проверяет статус теста и добавляет информацию о провале
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        item.rep_call = report
