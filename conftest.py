import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

GRID_URL = os.getenv("GRID_URL")           # kosong = jalan lokal
BROWSER = os.getenv("BROWSER", "chrome")   # chrome / firefox
HEADLESS = os.getenv("HEADLESS") == "1"    # dipakai di CI/CD


@pytest.fixture
def driver():
    if BROWSER == "firefox":
        opts = FirefoxOptions()
        if HEADLESS:
            opts.add_argument("-headless")
    else:
        opts = ChromeOptions()
        if HEADLESS:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")

    if GRID_URL:
        drv = webdriver.Remote(command_executor=GRID_URL, options=opts)
    elif BROWSER == "firefox":
        drv = webdriver.Firefox(options=opts)
    else:
        drv = webdriver.Chrome(options=opts)

    drv.implicitly_wait(0)
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Otomatis sisipkan screenshot ke report HTML kalau test gagal."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv:
            from pytest_html import extras
            shot = drv.get_screenshot_as_base64()
            report.extras = getattr(report, "extras", []) + [extras.png(shot)]