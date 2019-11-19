'''
'''
from selenium.common.exceptions import NoSuchElementException

from client_auth.CaptivePortal import CaptivePortal


class WebAuth(CaptivePortal):
    '''
    classdocs
    '''

    locators = {
        'username_textbox': r"//input[@name='username']",
        'password_textbox': r"//input[@name='password']",
        'login_button': r"//input[@name='ok']",
        'login_failed': r"//div[@id='loginfailed']",
    }


    def __init__(self):
        '''
        Constructor
        '''
        super(WebAuth, self).__init__()

    """
    def auth(self):
        '''
        '''
        super(WebAuth, self).auth()

        if self.is_client_authorized():
            return

        self.browser.get(self.params['dest_url'])

        try:
            textbox = self.browser.find_element_by_xpath(
                self.locators['username_textbox']
            )
            textbox.send_keys(self.params['username'])

            textbox = self.browser.find_element_by_xpath(
                self.locators['password_textbox']
            )
            textbox.send_keys(self.params['password'])

            button = self.browser.find_element_by_xpath(
                self.locators['login_button']
            )
            button.click()

        except NoSuchElementException as ex:
            self.message = ex.message
            return False

        #@author: anzuo, @change: wait "It works", max timeout is 25 sec, @since: 20140703
        import time
        timeout = 3
        base_timeout = 5
        while timeout < 25:
            time.sleep(timeout)
            super(WebAuth, self).auth()
        
            if self.is_client_authorized():
                return True
            else:
                timeout = timeout + base_timeout
        
        return False

    def is_login_successful(self):
        '''
        '''
        try:
            login_failed_div = self.browser.find_element_by_xpath(
                self.locators['login_failed']
            )

            self.message = login_failed_div.text
            return False

        except NoSuchElementException as ex:
            self.message = "Login is done."

        return True


    def deauth(self):
        '''
        '''
        return super(WebAuth, self).deauth()
    """
