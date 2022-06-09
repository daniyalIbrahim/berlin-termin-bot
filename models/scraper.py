
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,NoSuchElementException,ElementNotInteractableException,ElementClickInterceptedException,InvalidElementStateException
import time
from bs4 import BeautifulSoup
import logging
import threading
import platform
import psutil
import sys
from models.page import ScraperPage 

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
            self.logger.info(f"Error creating driver \n {e.msg} {e.args}")

    def scroll_helper(self,elem_id):
        """
        Helper function to scroll to an element with id
        """
        self.logger.info(f"{elem_id} is being scrolled")
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

    def init_logger(self)->logging.Logger:
        # create logger on the current module and set its level
        self.logger = logging.getLogger(__file__)
        self.logger.setLevel(logging.INFO)
        # create a formatter that creates a single line of json with a comma at the end
        formatter = logging.Formatter(
            (
                '["%(levelname)s"],"time":"%(asctime)s","module":"%(name)s",'
                '"line_no":%(lineno)s,"msg":"%(message)s"\n'
            )
        )
        # create a channel for handling the logger and set its format
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        # connect the logger to the channel
        ch.setLevel(logging.INFO)
        self.logger.addHandler(ch)
        # send an example message
        self.logger.info(f'initializing logger')
        self.logger.info(f' CPU : {platform.processor()}')
        self.logger.info(f' CPU COUNT: {psutil.cpu_count()}')
        self.logger.info(f' System: {sys.platform}')
        self.logger.info(f' Python version: {sys.version}')
        return self.logger

    def wait_for_page_load(self,wait_time=10):
        try:
            status = self.page_has_loaded()
            while status:
                self.driver.implicitly_wait(wait_time)
                wait_time += 1
                if wait_time >50:
                    self.logger.info("waited for 50 seconds for page to load")
                    wait_time=10
        except (Exception,TimeoutException) as e:
            self.logger.info(f"Timed out waiting for page to load \n {e.msg} {e.args}")

    def page_has_loaded(self)->bool:
        page = self.driver.find_element_by_tag_name('html')
        self.logger.info("Checking if {} page is loaded.".format(self.driver.current_url))
        try:
            new_page = self.driver.find_element_by_tag_name('html')
            self.logger.info(f"the page is loaded {new_page.id != page.id}")
            return new_page.id != page.id
        except Exception as e:
            self.logger.info(f"the page is loaded!")
            self.logger.info(f"Exception while loading {e.msg} {e.args}")
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
            self.logger.info(f"Exception while selecting option {e.msg} {e.args}")

    def click_btn_by_xpath(self,xpath_str,scroll_flag=0,delay=15):
        try:
            if scroll_flag == 1:
                self.driver.implicitly_wait(25)
                self.wait_for_page_load()
                time.sleep(5)
                elem = self.driver.find_element_by_xpath(xpath_str)
                self.scroll_helper(elem.get_attribute('id'))
                self.logger.info(f"scrolled successfully scrolled to {elem.tag_name()}")
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
                self.logger.info(f"scrolled successfully scrolled to {elem.tag_name()}")
            self.wait_for_page_load()
            click_btn = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH,xpath_str)))
            click_btn.click()
            self.logger.info(f"Exception while clicking {e.msg} {e.args}")
            

    def get_page_source(self)->str:
        return self.driver.page_source
    




class TerminScraper(GenericWebScraper):
    __slots__ = 'url','list_xpaths_to_click', 'list_xpaths_to_click_scroll', 'list_xpaths_to_select', 'list_xpaths_to_select_scroll','list_select_options','landing_page','information_page','service_page'

    def __init__(self,url,landing_page:ScraperPage,information_page:ScraperPage,service_page:ScraperPage, *args):
        super(GenericWebScraper, self).__init__(*args)
        self.logger = self.init_logger()
        self.driver_options = self.set_chrome_options()
        self.driver = self.create_driver()
        self.logger.info("TerminScraper is being initialized")
        self.url = url
        self.landing_page = landing_page
        self.information_page = information_page
        self.service_page = service_page

    def apply(self):
        try:
            self.driver.get(self.url)
            self.better_process()
        except Exception as e:
            self.logger.info(f"Error initializig process \n {e.msg} {e.args}")

    def better_process(self):
        self.logger.info("Starting better process")
        self.process_landing()
        time.sleep(2)
        self.process_information()
        time.sleep(2)
        self.process_service()
        time.sleep(2)
        
    def process_landing(self):
        self.logger.info("Starting landing page")
        c_xpaths = self.landing_page.get_list_xpaths_to_click()
        self.click_btn_by_xpath(xpath_str=c_xpaths[0])

    def process_information(self):
        self.logger.info("Starting information page")
        c_xpaths = self.information_page.get_list_xpaths_to_click()
        self.click_btn_by_xpath(xpath_str=c_xpaths[0])
        self.click_btn_by_xpath(xpath_str=c_xpaths[1])


    def process_service(self):
        self.logger.info("Starting Service page")
        s_xpaths = self.service_page.get_list_xpaths_to_select()
        s_option = self.service_page.get_list_select_options()
        self.select_dropdown_by_xpath(xpath_str=s_xpaths[0],value=s_option[0])
        self.select_dropdown_by_xpath(xpath_str=s_xpaths[1],value=s_option[1])
        self.select_dropdown_by_xpath(xpath_str=s_xpaths[2],value=s_option[2])
        c_xpaths = self.service_page.get_list_xpaths_to_click()
        self.click_btn_by_xpath(xpath_str=c_xpaths[0])
        cs_xpaths = self.service_page.get_list_xpaths_to_click_scroll()
        self.click_btn_by_xpath(xpath_str=cs_xpaths[0],scroll_flag=1)
        self.click_btn_by_xpath(xpath_str=c_xpaths[1])
        self.click_btn_by_xpath(xpath_str=cs_xpaths[1],scroll_flag=1)

    def process(self):
        try:
            self.wait_for_page_load()
            self.click_btn_by_xpath('//*[@id="mainForm"]/div/div/div/div/div/div/div/div/div/div[1]/div[1]/div[2]/a')
            self.logger.info(f"Page One is loaded successfully ")
            self.wait_for_page_load()
            self.click_btn_by_xpath('/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[4]/div[1]/div[4]/input')
            self.wait_for_page_load()
            self.click_btn_by_xpath('/html/body/div[2]/div[2]/div[4]/div[2]/form/div[5]/button')
            self.wait_for_page_load()
            self.logger.info(f"Page Two is loaded successfully ")
            self.wait_for_page_load()             
            self.select_dropdown_by_xpath(xpath_str='/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[2]/select',value="Pakistan")
            self.wait_for_page_load()
            self.select_dropdown_by_xpath(xpath_str='/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[3]/div[1]/div[1]/select',value="eine Person")
            self.wait_for_page_load()
            self.select_dropdown_by_xpath(xpath_str='/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[4]/select',value="nein")
            self.wait_for_page_load()
            self.click_btn_by_xpath('/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[9]/div[1]/div[1]/div[1]/div[1]/label')
            self.wait_for_page_load()
            self.click_btn_by_xpath('/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[9]/div[1]/div[1]/div[1]/div[6]/div/div[3]/label',scroll_flag=1)
            self.wait_for_page_load()
            self.click_btn_by_xpath('/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[9]/div[1]/div[1]/div[1]/div[6]/div/div[4]/div/div[11]/input')
            self.wait_for_page_load()
            self.click_btn_by_xpath('/html/body/div[2]/div[2]/div[4]/div[2]/form/div[5]/button',scroll_flag=1)
            self.logger.info(f"Page Three is loaded successfully ")
            self.wait_for_page_load()
            time.sleep(60)
        except TimeoutException as e:
            self.logger.info(f"Timed out waiting for page to load \n {e.msg} {e.args}")



    