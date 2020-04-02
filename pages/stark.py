import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from handy.tools import  Tools
from handy.useful_functions import username_generator, random_day, random_month, generate_mail, get_driver_path


class Stark:

    def __init__(self, email_username, person_info):
        self.path = get_driver_path()
        self.driver = webdriver.Chrome(executable_path=self.path)
        self.baseURL = 'http://starklibrary.org/home/contact-us/register-for-a-library-card/'
        self.person_info = person_info
        self.driver.get(self.baseURL)
        self.perform = Tools(self.driver)
        self.firstname = self.person_info["firstname"]
        self.lastname = self.person_info["lastname"]
        self.email_username = email_username
        # Locators
        self.first_name_ID = 'nfirst'
        self.nmiddle_ID = 'nmiddle'
        self.nlast_ID = 'nlast'
        self.street_addrs_ID = 'stre_aaddress'
        self.city_addrs_ID = 'city_aaddress'
        self.state_addrs_ID = 'stat_aaddress'
        self.postal_addrs_ID = 'post_aaddress'
        self.username_XPATH = '//*[@id="accessibleForm"]/form/fieldset/div[8]/input'
        self.birthdate_ID = 'F051birthdate'
        self.email_ID = 'zemailaddr'
        self.go_button_XPATH = '//*[@id="accessibleForm"]/form/fieldset/span/a'
        self.login_XPATH_ID = '//*[@id="topLinksList"]/li[1]/a'
        self.login_code_ID = 'code'
        self.login_pin_ID = 'pin'

        self.new_login_pin_ID = 'pin1'
        self.confirm_login_pin_ID = 'pin2'
        self.final_submit_XPATH_ID = '//*[@id="cas"]/div[1]/div[4]/a/div/div/span/span'
        # self.final_submit_XPATH_ID = '//*[contains(@span,"Submit")]'

    def _click_apply_Online_button(self):
        self.perform.click_by_LINK_TEXT('Apply online')

    def _set_firstName(self):
        self.perform.set_input_by_ID(self.first_name_ID, self.firstname)

    def _set_middle_name(self):
        self.perform.set_input_by_ID(self.nmiddle_ID, 'D')

    def _set_lastName(self):
        self.perform.set_input_by_ID(self.nlast_ID, self.lastname)

    def _set_address_info(self):
        street_address = self.person_info["street_adr"]
        city = self.person_info["city"]
        state = self.person_info["state"]
        postal_code = self.person_info["zipcode"]

        self.perform.set_input_by_ID(self.street_addrs_ID, street_address)
        self.perform.set_input_by_ID(self.city_addrs_ID, city)
        self.perform.set_input_by_ID(self.state_addrs_ID, state)
        self.perform.set_input_by_ID(self.postal_addrs_ID, postal_code)

    def _set_username(self):
        username = username_generator(13)
        self.perform.set_input_by_XPATH(self.username_XPATH, username)

    def _set_dob(self):
        dob_str = '{}-{}-1995'.format(random_month(), random_day())
        self.perform.set_input_by_ID(self.birthdate_ID, dob_str)

    def _set_email(self):
        error_flag = True
        while error_flag:
            try:
                error = WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_element_located((By.ID, 'selfRegMessage')))
                print(error.text)
                email = generate_mail(self.email_username)
                print(email)
                self.perform.set_input_by_ID(self.email_ID, email)
                error_flag = False
            except NoSuchElementException:
                error_flag = True
            except TypeError:
                error_flag = True

    def _click_go_button(self):
        self.perform.click_button_by_XPATH(self.go_button_XPATH)

    def _get_barcode(self):
        temp_list = []

        try:
            header = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'pageHeading')))

            elems = self.driver.find_elements(By.XPATH, '//strong')
            for elem in elems:
                temp_list.append(elem.text)
                return temp_list[0]
        except NoSuchElementException:
            return None

    def _fill_login_info(self, barcode):

        time.sleep(2)
        self.perform.set_input_by_ID(self.login_code_ID, barcode)
        self.perform.set_input_by_ID(self.login_pin_ID, '1234')

    def start_process(self):

        self._click_apply_Online_button()
        self._set_firstName()
        self._set_middle_name()
        self._set_lastName()
        self._set_address_info()
        self._set_username()
        self._set_dob()
        self._set_email()
        self._click_go_button()
        barcode = self._get_barcode()
        self._click_login()
        self._fill_login_info(barcode)
        self._click_submit()
        new_pin = self._create_new_pin(barcode)
        self._click_submit()
        self.print_save_info(barcode, new_pin)
        time.sleep(5)
        self.driver.close()
        self.driver.quit()

    def _create_new_pin(self, barcode):
        time.sleep(2)

        self._fill_login_info(barcode)
        new_pin = random.choice(range(1000, 10000))
        self.perform.set_input_by_ID(self.new_login_pin_ID, new_pin)
        self.perform.set_input_by_ID(self.confirm_login_pin_ID, new_pin)
        return new_pin

    def _click_submit(self):
        time.sleep(1)
        self.perform.click_button_by_XPATH(self.final_submit_XPATH_ID)

    def _click_login(self):
        WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Login'))
        ).click()

    def print_save_info(self, barcode, new_pin):
        print("===================================\n")

        print("Organization's URL ==> starklibrary.org\n")
        print("Barcode ==> {}\n".format(barcode))
        print("New PIN ==> {}\n".format(new_pin))

        print("===================================\n")
        print("library_card_info.txt saved in current folder")

        with open('library_card_info.txt', 'a') as txtfile:
            txtfile.writelines("===================================\n")
            txtfile.writelines("Created on ==> {}\n".format(time.ctime()))
            txtfile.writelines("Organization's URL ==> starklibrary.org\n")
            txtfile.writelines("Barcode ==> {}\n".format(barcode))
            txtfile.writelines("New PIN ==> {}\n".format(new_pin))
            txtfile.writelines("===================================\n")
