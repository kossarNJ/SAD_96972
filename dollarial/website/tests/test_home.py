from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

import time


class HomeTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')


    def test_home_contact_details(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/home/'))
        address = self.selenium.find_element_by_id("dollarial_address")
        phone = self.selenium.find_element_by_id("dollarial_phone")
        email = self.selenium.find_element_by_id("dollarial_email")
        self.assertIn("Department of Computer Enginerring, Sharif University of Technology", self.__get_text(address))
        self.assertIn("21 6600 5616", self.__get_text(phone))
        self.assertIn("dollarialsharif@gmail.com", self.__get_text(email))