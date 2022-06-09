
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException,TimeoutException,NoSuchElementException,ElementNotInteractableException,ElementClickInterceptedException
import time
import threading
from logger.index import infoLogger

# Logger Settings
PAGE_TIMEOUT =25
TIMEOUT=15

class GenericWebScraper:
    __slots__ = 'driver', 'driver_options', 'url', 'logger'

    def __init__(self, url):
        self.url = url
        
    def create_driver(self) -> webdriver:
        """returns a new chrome webdriver"""
        try:
            if self.driver_options is None:
                self.set_chrome_options()
            self.driver = webdriver.Chrome(executable_path="./driver/win32/chromedriver", options=self.driver_options)
            return self.driver
        except Exception as e:
            infoLogger.info(f"Error creating driver \n {e.msg} {e.args}")

    def scroll_helper(self,elem_id):
        """
        Helper function to scroll to an element with id
        """
        infoLogger.info(f"{elem_id} is being scrolled")
        elem_fstr = "document.getElementById({}).scrollIntoView();".format(elem_id)
        self.driver.execute_script(elem_fstr)

    def set_chrome_options(self) -> Options:
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #chrome_prefs = {}
        #chrome_options.experimental_options["prefs"] = chrome_prefs
        #chrome_prefs["excludeSwitches"] =  ['enable-logging']
        return chrome_options

    def wait_for_page_load(self,wait_time=10):
        try:
            status = self.page_has_loaded()
            while status:
                self.driver.implicitly_wait(wait_time)
                wait_time += 1
                if wait_time >50:
                    infoLogger.info("waited for 50 seconds for page to load")
                    wait_time=10
        except (Exception,TimeoutException) as e:
            infoLogger.info(f"Timed out waiting for page to load \n {e.msg} {e.args}")

    def page_has_loaded(self)->bool:
        page = self.driver.find_element_by_tag_name('html')
        infoLogger.info("Checking if {} page is loaded.".format(self.driver.current_url))
        try:
            new_page = self.driver.find_element_by_tag_name('html')
            infoLogger.info(f"the page is loaded {new_page.id != page.id}")
            return new_page.id != page.id
        except Exception as e:
            infoLogger.info(f"the page is loaded!")
            infoLogger.info(f"Exception while loading {e.msg} {e.args}")
            return False

    def select_dropdown_by_xpath(self,xpath_str,value,delay=100):
        """
            Selects an option from a dropdown by xpath.
        """
        try:
            self.driver.implicitly_wait(25)
            self.wait_for_page_load()
            time.sleep(5)
            dropdown = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath_str)))
            for option in dropdown.find_elements_by_tag_name('option'):
                if option.text == value:
                    option.click() # select() in earlier versions of webdriver
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            self.driver.implicitly_wait(25)
            self.wait_for_page_load()
            time.sleep(5)
            dropdown = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath_str)))
            for option in dropdown.find_elements_by_tag_name('option'):
                if option.text == value:
                    option.click() # select() in earlier versions of webdriver
            infoLogger.info(f"Exception while selecting option {e.msg} {e.args}")

    def click_btn_by_xpath(self,xpath_str,scroll_flag=0,delay=15):
        try:
            if scroll_flag == 1:
                self.driver.implicitly_wait(25)
                self.wait_for_page_load()
                time.sleep(5)
                elem = self.driver.find_element_by_xpath(xpath_str)
                self.scroll_helper(elem.get_attribute('id'))
                infoLogger.info(f"scrolled successfully scrolled to {elem.tag_name()}")
            self.wait_for_page_load()
            click_btn = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH,xpath_str)))
            click_btn.click()
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            if scroll_flag == 1:
                self.driver.implicitly_wait(25)
                self.wait_for_page_load()
                time.sleep(5)
                elem = self.driver.find_element_by_xpath(xpath_str)
                self.scroll_helper(elem.get_attribute('id'))
                infoLogger.info(f"scrolled successfully scrolled to {elem.tag_name()}")
            self.wait_for_page_load()
            click_btn = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH,xpath_str)))
            click_btn.click()
            infoLogger.info(f"Exception while clicking {e.msg} {e.args}")
    
    def find_element(self,elementXpath, elementName):
        pageTimer = 0
        while(1):
            try:
                element = self.driver.find_element_by_xpath(elementXpath)
                infoLogger.info(f"Succeded to find the element {elementName}")
                return element
            except(NoSuchElementException, ElementNotInteractableException):
                infoLogger.info(f"Looking for the element: {elementName}")
            except(WebDriverException):
                infoLogger.info(f"Failed to reach webDriver")
            if(pageTimer > PAGE_TIMEOUT):
                infoLogger.info("Failed to load the page withim limit")
                return False
            pageTimer += 1
            time.sleep(1)

    def click_element(self,element, elementName):
        pageTimer = 0
        while(1):
            if(element.is_enabled()):
                try:
                    element.click()
                    infoLogger.info(f"Succeded to click {elementName}")
                    return True
                except(ElementNotInteractableException):
                    infoLogger.info(f"Element:{elementName} is not Interactable yet")
                    pass
                except(WebDriverException):
                    infoLogger.info(f"Failed to reach webDriver")
            if(not element.is_enabled()):
                infoLogger.info(
                    f"waiting for the element:{elementName} to be enabled")
            if(pageTimer > PAGE_TIMEOUT):
                infoLogger.info(
                    f"Failed to enable the element:{elementName} within the limit")
                return False
            pageTimer += 1
            time.sleep(1)


    def select_value(self,element, elementName, elementValue):
        pageTimer = 0
        while(1):
            try:
                Select(element).select_by_value(elementValue)
                infoLogger.info(f"Succeded to select value: {elementValue}")
                return True
            except(NoSuchElementException, ElementNotInteractableException):
                infoLogger.info(f"Looking for the element: {elementName}")
            except(WebDriverException):
                infoLogger.info(f"Failed to reach webDriver")
            if(pageTimer > PAGE_TIMEOUT):
                infoLogger.info(
                    f"Failed to enable the element:{elementName} within the limit")
                return False
            pageTimer += 1
            time.sleep(1)


    def find_and_select_element(self,elementXpath, elementName, elementValue):
        element = self.find_element(elementXpath, elementName)
        time.sleep(2)
        if(element):
            return self.select_value(element, elementName, elementValue)
        else:
            return False


    def find_and_click_element(self, elementXpath, elementName):
        element = self.find_element( elementXpath, elementName)
        time.sleep(2)
        if(element):
            return self.click_element(element, elementName)
        else:
            return False


            

    def get_page_source(self)->str:
        return self.driver.page_source
    
    def run_multi_threaded(self):
        start_time = time.time()
        threads = []
        for i in range(10):
            th = threading.Thread(target=self.run_thread)
            th.start()  # could `time.sleep` between 'clicks' to see whats'up without headless option
            threads.append(th)
        for th in threads:
            th.join()  # Main thread wait for threads finish
        infoLogger.info("multiple threads took ", (time.time() - start_time), " seconds")

    def get_driver(self):
        return self.driver




