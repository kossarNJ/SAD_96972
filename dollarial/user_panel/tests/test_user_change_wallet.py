from importlib import import_module

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from dollarial.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.conf import settings


class ChangeWalletTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username="kossar",
                                             email="k_na@gmail.com",
                                             password="likeicare",
                                             first_name="kossar",
                                             last_name="najafi",
                                             phone_number="09147898557",
                                             account_number="1234432112344321",
                                             notification_preference="S")
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/charge/'))

    def __get_page(self):
        class IndexPage(object):
            def __init__(self, selenium):
                self.selenium = selenium
                self.charge_amount = self.selenium.find_element_by_id('id_amount')
                self.charge_button = self.selenium.find_element_by_id('charge-button')

        return IndexPage(self.selenium)

    def login(self):
        user = User.objects.get(username="kossar")
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        session = SessionStore()
        session[SESSION_KEY] = User.objects.get(username="kossar").id
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()

        cookie = {
            'name': settings.SESSION_COOKIE_NAME,
            'value': session.session_key,
            'path': '/',
        }

        self.selenium.add_cookie(cookie)
        self.selenium.refresh()
        self.selenium.get('%s%s' % (self.live_server_url, '/user_panel/charge/'))

    @staticmethod
    def _fill(page):
        page.charge_amount.clear()
        page.charge_amount.send_keys('59000')

    @staticmethod
    def __get_text(element):
        return element.get_attribute('textContent')

    def test_charge_wallet_successful(self):
        self.login()
        page = self.__get_page()
        self._fill(page)
        page.charge_button.click()
        success = self.selenium.find_element_by_xpath('//*[@id="right-panel"]/div[2]/div/div[1]/div/div')
        self.assertIn("Wallet is charged successfully.", self.__get_text(success))

    def test_charge_wallet_unsuccessful(self):
        self.login()
        page = self.__get_page()
        self._fill(page)
        page.charge_amount.clear()
        page.charge_button.click()
        success_set = self.selenium.find_elements_by_xpath('//*[@id="right-panel"]/div[2]/div/div[1]/div/div')
        self.assertEqual(len(success_set), 0)
