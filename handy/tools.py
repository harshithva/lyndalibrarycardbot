from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from handy.useful_functions import clear_text_box


class Tools:

    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(30)

    def set_date_box(self, month=None, day=None, year=None, month_id=None, day_id=None, year_id=None):

        if month_id != None:
            select_month_box = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, month_id)))
            select_month = Select(select_month_box)
            select_month.select_by_value(month)

        if day_id != None:
            select_day_box = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, day_id)))
            select_day = Select(select_day_box)
            select_day.select_by_value(day)

        if year_id != None:
            select_year_box = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, year_id)))
            select_year = Select(select_year_box)
            select_year.select_by_value(year)

    def click_button_by_XPATH(self, button_XPATH):
        # WebDriverWait(self.driver, 40).until(
        #     EC.presence_of_element_located((By.XPATH, button_XPATH))).click()
        actionchains = ActionChains(self.driver)
        btn_elem = WebDriverWait(self.driver, 40).until(
            EC.presence_of_element_located((By.XPATH, button_XPATH)))
        actionchains.move_to_element(btn_elem).click(btn_elem).perform()

    def click_button_by_ID(self, button_ID):
        actionchains = ActionChains(self.driver)
        btn_elem = WebDriverWait(self.driver, 40).until(
            EC.presence_of_element_located((By.ID, button_ID)))
        actionchains.move_to_element(btn_elem).click(btn_elem).perform()

    def set_input_by_ID(self, input_box_id, input_value):
        input_box = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, input_box_id))
        )
        clear_text_box(input_box)
        input_box.send_keys(input_value)

    def set_input_by_XPATH(self, input_box_XPATH, input_value):
        input_box = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, input_box_XPATH))
        )
        clear_text_box(input_box)
        input_box.send_keys(input_value)

    def click_by_LINK_TEXT(self, text):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, text))
        ).click()

    def set_select_by_ID(self, select_ID, value):
        try:
            box = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, select_ID)))
            option = Select(box)
            option.select_by_value(value)
        except NoSuchElementException:
            print("Not found anything to select")

    def set_select_by_NAME(self, select_NAME, value):
        try:
            box = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.NAME, select_NAME)))
            option = Select(box)
            option.select_by_value(value)
        except NoSuchElementException:
            print("Not found anything to select")

    def set_select_by_CLASS(self, class_name, value):
        box = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name)))

        option = Select(box)
        option.select_by_value(value)

    #################################################################################################
