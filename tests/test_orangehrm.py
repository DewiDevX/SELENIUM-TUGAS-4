import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage


def do_login(driver):
    page = LoginPage(driver)
    page.open()
    page.login()
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//h6[normalize-space()='Dashboard']"))
    )


def test_login_valid_credentials(driver):
    do_login(driver)
    assert "OrangeHRM" in driver.title
    assert "dashboard" in driver.current_url


def test_login_invalid_credentials(driver):
    page = LoginPage(driver)
    page.open()
    page.login("Admin", "salah123")
    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".oxd-alert-content-text"))
    )
    assert "Invalid credentials" in error.text


# (nama menu di sidebar, judul header yang diharapkan)
MENUS = [
    ("Admin", "Admin"),
    ("PIM", "PIM"),
    ("Leave", "Leave"),
    ("Time", "Time"),
    ("Recruitment", "Recruitment"),
    ("Performance", "Performance"),
    ("Dashboard", "Dashboard"),
    ("Directory", "Directory"),
    ("Claim", "Claim"),
    ("Buzz", "Buzz"),
]


@pytest.mark.parametrize("menu,header", MENUS)
def test_navigasi_menu(driver, menu, header):
    do_login(driver)
    driver.find_element(
        By.XPATH, f"//span[text()='{menu}']").click()
    WebDriverWait(driver, 15).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb"), header)
    )


def test_logout(driver):
    do_login(driver)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".oxd-userdropdown-tab"))).click()
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[text()='Logout']"))).click()
    wait.until(EC.url_contains("auth/login"))
    assert "auth/login" in driver.current_url