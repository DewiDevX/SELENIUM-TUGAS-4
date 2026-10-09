import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SERVICES_URL = "https://ultimateqa.com/consulting/"


def klik_menu(driver, wait, link_text):
    """Klik menu berdasarkan teks link, lewat JS agar tidak terhalang overlay."""
    el = wait.until(EC.presence_of_element_located((By.LINK_TEXT, link_text)))
    driver.execute_script("arguments[0].click();", el)
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 15)


def test_01_services(driver, wait):
    driver.get(SERVICES_URL)
    h1 = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
    assert ("World's Best Test Automation Solutions" in h1.text
            or "Consulting" in h1.text)


def test_02_case_studies(driver, wait):
    driver.get(SERVICES_URL)
    klik_menu(driver, wait, "Case Studies")
    assert "case-studies" in driver.current_url.lower()


def test_03_blog_search(driver, wait):
    driver.get(SERVICES_URL)
    klik_menu(driver, wait, "Blog")
    assert "blog" in driver.current_url.lower()

    # Ambil kolom search yang benar-benar terlihat (ada beberapa elemen name='s')
    kolom = driver.find_elements(By.NAME, "s")
    terlihat = [e for e in kolom if e.is_displayed()]

    if terlihat:
        search = terlihat[0]
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", search)
        search.send_keys("Selenium")
        assert search.get_attribute("value") == "Selenium"
    else:
        # Kolom search tersembunyi: isi lewat JavaScript
        search = kolom[0]
        driver.execute_script("arguments[0].value = 'Selenium';", search)
        assert search.get_attribute("value") == "Selenium"


def test_04_education_fill_forms(driver, wait):
    driver.get(SERVICES_URL)
    klik_menu(driver, wait, "Automation Exercises")
    link = wait.until(EC.presence_of_element_located(
        (By.LINK_TEXT, "Fill out forms")))
    driver.execute_script("arguments[0].click();", link)

    nama = wait.until(EC.visibility_of_element_located(
        (By.ID, "et_pb_contact_name_0")))
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", nama)
    nama.send_keys("Praktikum Selenium WebDriver")
    pesan = wait.until(EC.visibility_of_element_located(
        (By.ID, "et_pb_contact_message_0")))
    pesan.send_keys("Pengujian Selenium Grid selesai.")

    assert nama.get_attribute("value") == "Praktikum Selenium WebDriver"
    assert pesan.get_attribute("value") == "Pengujian Selenium Grid selesai."