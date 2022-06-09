
import time
from models.scraper import GenericWebScraper 
from logger.index import infoLogger
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, UnexpectedAlertPresentException, WebDriverException
from random import randint



class TerminScraper(GenericWebScraper):
    __slots__ = 'url',"time_out","page_timeout"

    def __init__(self,url,t_out,p_out,*args):
        super(GenericWebScraper, self).__init__(*args)
        self.driver_options = self.set_chrome_options()
        self.driver = self.create_driver()
        infoLogger.info("TerminScraper is being initialized")
        self.url = url
        self.time_out=t_out
        self.page_timeout=p_out


    def get_home_page(self):
        try:
            self.driver.get(self.url)
            infoLogger.info("Main page is succeed to request")
            time.sleep(1)
            return True
        except:
            infoLogger.info("Main page is failed  to request")
            return False
    
    def click_book_appointment_button(self):
        # Click to Book appointment
        elementXpath = '//*[@id="mainForm"]/div/div/div/div/div/div/div/div/div/div[1]/div[1]/div[2]/a'
        elementName = "book appointment button"
        return self.find_and_click_element( elementXpath, elementName)


    def click_accept_terms_checkbox(self):
        elementXpath = '//*[@id="xi-cb-1"]'
        elementName = "accept terms checkbox"
        return self.find_and_click_element( elementXpath, elementName)


    def click_accept_terms_button(self):
        elementXpath = '//*[@id="applicationForm:managedForm:proceed"]'
        elementName = "accept terms button"
        return self.find_and_click_element( elementXpath, elementName)


    def set_citizenship(self):
        """"
        set the country from the dropdown menu
        """
        elementXpath = '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[2]/select'
        elementName = "Citizenship"
        return self.find_and_select_element( elementXpath, elementName, "461")


    def set_applicants_number(self):
        """"
        set the Number of applicants who need a residence title (inluding foreign spouse and children)
        """
        elementXpath = '//*[@id="xi-sel-422"]'
        elementName = "Applications Count"
        return self.find_and_select_element( elementXpath, elementName, "1")


    def set_family(self):
        elementXpath = '//*[@id="xi-sel-427"]'
        elementName = "Family member"
        return self.find_and_select_element( elementXpath, elementName, "2")


    def set_visa_group(self):
        elementXpath = '//*[@id="xi-div-30"]/div[1]/label/p'
        elementName = "set visa group"
        return self.find_and_click_element( elementXpath, elementName)


    def set_visa_type(self):
        elementXpath = '//*[@id="inner-461-0-1"]/div/div[3]/label'
        elementName = "set visa type"
        return self.find_and_click_element( elementXpath, elementName)


    def set_blue_card(self):
        elementXpath = '//*[@id="inner-461-0-1"]/div/div[4]/div/div[1]/label'
        elementName = "click blue card"
        return self.find_and_click_element( elementXpath, elementName)


    def set_qualified_skilled_with_ae(self):
        # Click to Book appointment
        elementXpath = '//*[@id="SERVICEWAHL_EN163-0-1-1-329328"]'
        elementName = "qualifiedSkilled"
        return self.find_and_click_element( elementXpath, elementName)


    def click_next(self):
        elementXpath = '//*[@id="applicationForm:managedForm:proceed"]'
        elementName = "next button"
        return self.find_and_click_element( elementXpath, elementName)

    def check_availability(self):
        elementXpath = '/html/body/div[2]/div[2]/div[3]/ul/li/'
        elementName = "next button"
        element = self.find_and_click_element( elementXpath, elementName)
        if element is not None:
            infoLogger.info(f"{element.text}")
    
    def handle_error(self):
        # Check Error Message
        pageTimer = 0
        elementXpath = '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div/div[1]/div[3]/div[1]/fieldset/legend'
        while(1):
            try:
                if(self.driver.find_element_by_class_name("errorMessage")):
                    infoLogger.info(
                        f"No appointment, starting to process again in {self.time_out} seconds ...")
                    self.check_availability()
                    time.sleep(self.time_out)
                    return False
                if(pageTimer > self.page_timeout):
                    infoLogger.info("Failed to load the page withim limit")
                    return False
                else:
                    sourceHtml = self.driver.page_source
                    f = open("source-"+str(randint(1,100))+".html","w")
                    f.write(sourceHtml)
                    f.close()
                    infoLogger.info("FOUND IT")
                    return True
            except(NoSuchElementException, ElementNotInteractableException):
                infoLogger.info("Page is loading")
            except(UnexpectedAlertPresentException):
                infoLogger.warn("Someproblem happend ")
                return True
            except(WebDriverException):    
                infoLogger.info("Error on finding the driver")
                pass
            time.sleep(1)
            pageTimer += 1

    

    