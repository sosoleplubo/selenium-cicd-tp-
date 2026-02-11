import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from calculator_page import CalculatorPage


@pytest.fixture(scope="class")
def driver():
    chrome_options = Options()

    if os.getenv('CI'):
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    yield driver
    driver.quit()


@pytest.fixture
def calculator(driver):
    page = CalculatorPage(driver)
    page.load_page()
    return page


class TestCalculator:

    def test_page_loads(self, calculator):
        assert "Calculatrice Simple" in calculator.driver.title

    def test_addition(self, calculator):
        calculator.enter_first_number(10)
        calculator.enter_second_number(5)
        calculator.select_operation("add")
        calculator.click_calculate()

        assert "Résultat: 15" in calculator.get_result()

    def test_division_by_zero(self, calculator):
        calculator.enter_first_number(10)
        calculator.enter_second_number(0)
        calculator.select_operation("divide")
        calculator.click_calculate()

        assert "Erreur: Division par zéro" in calculator.get_result()

    def test_all_operations(self, calculator):
        operations = [
            ("add", 8, 2, "10"),
            ("subtract", 8, 2, "6"),
            ("multiply", 8, 2, "16"),
            ("divide", 8, 2, "4")
        ]

        for op, n1, n2, expected in operations:
            calculator.enter_first_number(n1)
            calculator.enter_second_number(n2)
            calculator.select_operation(op)
            calculator.click_calculate()

            assert f"Résultat: {expected}" in calculator.get_result()

    def test_page_load_time(self, calculator):
        start = time.time()
        calculator.load_page()
        load_time = time.time() - start

        assert load_time < 3