import random
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from handy.tools import Tools
from handy.useful_functions import new_tab, switch_to, get_driver_path, clear


class AccountDetail:

    def __init__(self, get_state):
        self.path = get_driver_path()
        self.driver = webdriver.Chrome(executable_path=self.path)
        # self.driver.maximize_window()
        self.get_state = get_state
        self._firstname = None
        self._fatherName = None
        self._lastname = None
        self._sex = None
        self._ssn = None
        self._phone_num = None
        self._parent_phone_num = None
        self._street_address = None
        self._city = None
        self._state = None
        self.zip_code = None

    def get_state_value(self):
        state_value = {
            "Alaska": "AK",
            "Alabama": "AL",
            "Arkansas": "AR",
            "Arizona": "AZ",
            "California": "CA",
            "Colorado": "CO",
            "Connecticut": "CT",
            "District of Columbia": "DC",
            "Delaware": "DE",
            "Florida": "FL",
            "Georgia": "GA",
            "Hawaii": "HI",
            "Iowa": "IA",
            "Idaho": "ID",
            "Illinois": "IL",
            "Indiana": "IN",
            "Kansas": "KS",
            "Kentucky": "KY",
            "Louisiana": "LA",
            "Massachusetts": "MA",
            "Maryland": "MD",
            "Maine": "ME",
            "Michigan": "MI",
            "Minnesota": "MN",
            "Missouri": "MO",
            "Mississippi": "MS",
            "Montana": "MT",
            "North Carolina": "NC",
            "North Dakota": "ND",
            "Nebraska": "NE",
            "New Hampshire": "NH",
            "New Jersey": "NJ",
            "New Mexico": "NM",
            "Nevada": "NV",
            "New York": "NY",
            "Ohio": "OH",
            "Oklahoma": "OK",
            "Oregon": "OR",
            "Pennsylvania": "PA",
            "Rhode Island": "RI",
            "South Carolina": "SC",
            "South Dakota": "SD",
            "Tennessee": "TN",
            "Texas": "TX",
            "Utah": "UT",
            "Virginia": "VA",
            "Vermont": "VT",
            "Washington": "WA",
            "Wisconsin": "WI",
            "West Virginia": "WV",
            "Wyoming": "WY"
        }
        return state_value.get(self.get_state.lower().title())

    def _generate_names(self):
        clear()
        print("Generating names......")
        perform = Tools(self.driver)
        baseURL = 'https://www.fakenamegenerator.com/'
        self.driver.get(baseURL)

        name_XPATH = '//div[@class ="address"]/h3'
        sex_value = random.choice(['male', 'female'])
        time.sleep(2)
        print("grabing student name....")
        name = None
        father_fullname = None
        while name is None:
            try:
                perform.set_select_by_ID('gen', sex_value)
                time.sleep(2)
                perform.click_button_by_ID('genbtn')
                name = WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, name_XPATH))).text
            except Exception as e:
                print(e)
        print("Got Student name ☺!")
        while father_fullname is None:
            try:
                perform.set_select_by_ID('gen', 'male')
                time.sleep(2)
                perform.click_button_by_ID('genbtn')
                father_fullname = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, name_XPATH))).text
            except Exception as e:
                print(e)

        father_fullname = father_fullname.split()
        print("Got Father name ☺!")

        self._firstname = name.split()[0]
        self._fatherName = father_fullname[0]
        self._lastname = father_fullname[2]
        if sex_value == 'male':
            self._sex = 'M'
        else:
            self._sex = 'F'

    def generate_address(self):
        print("Generating Address....")
        switch_to(self.driver, 'fakenamegenerator')

        perform = Tools(self.driver)

        generate_btn_ID = 'genbtn'
        address_XPATH = '//div[@class="adr"]'

        perform.click_by_LINK_TEXT('Advanced Options')
        perform.click_by_LINK_TEXT('Switch to Region')
        select_region_XPATH = '//select/optgroup[@label="United States"]/option'

        select_option_elem = WebDriverWait(self.driver, 40).until(
            EC.presence_of_all_elements_located((By.XPATH, select_region_XPATH)))

        actions = ActionChains(self.driver)

        for option in select_option_elem:
            if option.text.lower() == self.get_state.lower():
                actions.double_click(option).perform()
                break

        perform.click_button_by_ID(generate_btn_ID)
        time.sleep(5)
        address_elem = WebDriverWait(self.driver, 40).until(
            EC.presence_of_element_located((By.XPATH, address_XPATH)))
        time.sleep(2)

        address = address_elem.text  # address = ['2574 Middleville Road', 'City Of Commerce, CA 90040']
        address = address.splitlines()
        street_address = address[0]  # street_address = '2574 Middleville Road'
        city_state_zip = address[1]  # city_state_zip = 'City Of Commerce, CA 90040'
        city = city_state_zip.split(',')[0]

        state_zip = city_state_zip.split(',')[1]  # state_zip = ' CA 90040'

        state = state_zip.strip().split()[0]
        zipcode = state_zip.strip().split()[1]

        print("Got Address ☺!")
        self._street_address = street_address
        self._city = city
        self._state = state
        self.zip_code = zipcode

    def _generate_ssn(self):
        print("Generating SSN....")
        baseURL = 'https://www.ssn-verify.com/generate'
        perform = Tools(self.driver)
        state_control_ID = 'state'
        year_control_ID = 'year'
        btn_submit_ID = 'ssn-submit'
        result_ssn_CLASS_NAME = 'result-ssn'

        new_tab(self.driver, baseURL)
        switch_to(self.driver, 'generate')

        perform.set_select_by_ID(state_control_ID, self.get_state.lower())
        time.sleep(1.3)
        perform.set_select_by_ID(year_control_ID, "1997")
        # time.sleep(4)
        perform.click_button_by_ID(btn_submit_ID)

        # time.sleep(3)
        while True:
            ssn_number = WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.CLASS_NAME, result_ssn_CLASS_NAME))).text
            perform.click_button_by_ID(btn_submit_ID)
            time.sleep(1)
            if ssn_number != 'XXX-XX-XXXX':
                break
        print("Got SSN ☺!")
        self._ssn = ssn_number

    def _generate_phone_number(self):
        print("Generating phone numbers....")
        short_state = self.get_state_value()
        baseURL = 'https://www.fakephonenumber.org/UnitedStates/phone_number_generator?state=' + short_state

        new_tab(self.driver, baseURL)
        switch_to(self.driver, 'fakephonenumber')

        phone_numbers_elem = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@class="numbers"]')))
        phone_list = []
        for p in phone_numbers_elem:
            if p.text.split(':')[0] == 'Mobile':
                phone_list.append(p.text.split(':')[1].strip())
        print("Got Phone numbers ☺!")
        self._phone_num = random.choice(phone_list)
        self._parent_phone_num = random.choice(phone_list)

    def get_student_info(self):
        info = {}
        self._generate_names()
        self.generate_address()
        # self._generate_ssn()
        # self._generate_phone_number()

        print("Done generating student info ☺!")
        info["firstname"] = self._firstname
        info["lastname"] = self._lastname
        info["sex"] = self._sex
        info["ssn"] = self._ssn
        info["fathername"] = self._fatherName
        info["phone_num"] = self._phone_num
        info["parent_phone"] = self._parent_phone_num
        info["street_adr"] = self._street_address
        info["city"] = self._city
        info["state"] = self._state
        info["zipcode"] = self.zip_code

        self.driver.quit()
        return info
