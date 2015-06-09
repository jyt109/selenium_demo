from selenium import webdriver
import os
from pw import pw
import time
from helper import selector, load_jquery, scroll_to_bottom, get_outerhtml, alert
from bs4 import BeautifulSoup


class StartAndLogin(object):

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.base_url = 'https://www.facebook.com/'
        self.driver = None

    def start_driver(self):
        path = os.path.join(os.getcwd(), 'chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        # Start the driver and assign to instance variable
        driver = webdriver.Chrome(executable_path=path, chrome_options=options)
        self.driver = driver
        # Go to facebook's landing page
        driver.get(self.base_url)
        # Whenever you load a new page in FB, you must reload the jquery
        load_jquery(self.driver)

    def login(self):
        email_select = '#email'
        password_select = '#pass'

        email_div = selector(self.driver, email_select)
        email_div.send_keys(self.email)

        password_div = selector(self.driver, password_select)
        password_div.send_keys(self.password)
        password_div.submit()
        time.sleep(3)
        load_jquery(self.driver)

    def run(self):
        self.start_driver()
        self.login()
        return self.driver


class GetUID(object):
    def __init__(self, email, pw):
        self.driver = StartAndLogin(email, pw).run()

    def profile_page(self):
        selector(self.driver, '.fbxWelcomeBoxName').click()
        load_jquery(self.driver)

    def friends_page(self):
        selector(self.driver, '._5opl:contains("Friends")').click()
        load_jquery(self.driver)

    def get_uid(self):
        uid_query = '.fsl.fwb.fcb'
        bottom = scroll_to_bottom(self.driver, uid_query)
        if bottom:
            return get_outerhtml(self.driver, uid_query)


class ScrapeInfoFromUID(object):

    def __init__(self):
        pass


obj = GetUID('jeffrey.tang09@gmail.com', pw())
obj.profile_page()
obj.friends_page()
lst = obj.get_uid()
