from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, UnexpectedAlertPresentException, WebDriverException
from datetime import datetime
import os
import logging
from datetime import datetime
from random import randint
import sys

# Logger Settings
PAGE_TIMEOUT =25
TIMEOUT=15
def initLogger(logLevel):
    def getLoggerName(logLevel):
        logName=""
        if(logLevel==logging.INFO):logName="info" 
        if(logLevel==logging.ERROR):logName="error"
        if(logLevel==logging.DEBUG):logName="debug"
        return logName

    def initLogFilePath(logName):
        currentTime = datetime.now()
        currentTimeString= currentTime.strftime("%Y-%m-%d %H:%M:%S")
        LogFilePath = "log/"+logName+"_"+currentTimeString+".log"
        return LogFilePath

    def setLogger(testLogger,logLevel):
        logFilePath = initLogFilePath(getLoggerName(logLevel))
        streamHandler = logging.StreamHandler(sys.stdout)
        #fileHandler = logging.FileHandler(logFilePath, mode = 'a')
        streamFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        fileFormatter = logging.Formatter('%(asctime)s,%(levelname)s,%(message)s', datefmt='%H:%M:%S')
        streamHandler.setFormatter(streamFormatter)
        #fileHandler.setFormatter(fileFormatter)
        testLogger.addHandler(streamHandler)
        #testLogger.addHandler(fileHandler)
        return testLogger

    testLogger = logging.getLogger('logger_'+str(randint))
    testLogger.setLevel(logLevel)
    mylogger = setLogger(testLogger,logLevel)
    return mylogger

myLogger = initLogger(logging.INFO)

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


def findElement(driver, elementXpath, elementName):
    pageTimer = 0
    while(1):
        try:
            element = driver.find_element_by_xpath(elementXpath)
            myLogger.info(f"Succeded to find the element {elementName}")
            return element
        except(NoSuchElementException, ElementNotInteractableException):
            myLogger.info(f"Looking for the element: {elementName}")
        except(WebDriverException):
            myLogger.info(f"Failed to reach webDriver")
        if(pageTimer > PAGE_TIMEOUT):
            myLogger.info("Failed to load the page withim limit")
            return False
        pageTimer += 1
        time.sleep(1)


def clickElement(element, elementName):
    pageTimer = 0
    while(1):
        if(element.is_enabled()):
            try:
                element.click()
                myLogger.info(f"Succeded to click {elementName}")
                return True
            except(ElementNotInteractableException):
                myLogger.info(f"Element:{elementName} is not Interactable yet")
                pass
            except(WebDriverException):
                myLogger.info(f"Failed to reach webDriver")

            except(WebDriverException):
                myLogger.info(f"Failed to reach webDriver")
        if(not element.is_enabled()):
            myLogger.info(
                f"waiting for the element:{elementName} to be enabled")
        if(pageTimer > PAGE_TIMEOUT):
            myLogger.info(
                f"Failed to enable the element:{elementName} within the limit")
            return False

        pageTimer += 1
        time.sleep(1)


def selectValue(element, elementName, elementValue):
    pageTimer = 0
    while(1):
        try:
            Select(element).select_by_value(elementValue)
            myLogger.info(f"Succeded to select value: {elementValue}")
            return True
        except(NoSuchElementException, ElementNotInteractableException):
            myLogger.info(f"Looking for the element: {elementName}")
        except(WebDriverException):
            myLogger.info(f"Failed to reach webDriver")
        if(pageTimer > PAGE_TIMEOUT):
            myLogger.info(
                f"Failed to enable the element:{elementName} within the limit")
            return False
        pageTimer += 1
        time.sleep(1)


def findAndSelectElement(driver, elementXpath, elementName, elementValue):
    element = findElement(driver, elementXpath, elementName)
    time.sleep(2)
    if(element):
        return selectValue(element, elementName, elementValue)
    else:
        return False


def findAndClickElement(driver, elementXpath, elementName):
    element = findElement(driver, elementXpath, elementName)
    time.sleep(2)
    if(element):
        return clickElement(element, elementName)
    else:
        return False


def getHomePage(driver):
    try:
        driver.get("https://otv.verwalt-berlin.de/ams/TerminBuchen?lang=en")
        myLogger.info("Main page is succeed to request")
        time.sleep(1)
        return True
    except:
        myLogger.info("Main page is failed  to request")
        return False


def clickBookAppointmentButton(driver):
    # Click to Book appointment
    elementXpath = '//*[@id="mainForm"]/div/div/div/div/div/div/div/div/div/div[1]/div[1]/div[2]/a'
    elementName = "book appointment button"
    return findAndClickElement(driver, elementXpath, elementName)


def clickAcceptTermsCheckbox(driver):
    elementXpath = '//*[@id="xi-cb-1"]'
    elementName = "accept terms checkbox"
    return findAndClickElement(driver, elementXpath, elementName)


def clickAcceptTermsButton(driver):
    elementXpath = '//*[@id="applicationForm:managedForm:proceed"]'
    elementName = "accept terms button"
    return findAndClickElement(driver, elementXpath, elementName)


def setCitizenship(driver):
    """"
    set the country from the dropdown menu
    """
    elementXpath = '//*[@id="xi-sel-400"]'
    elementName = "Citizenship"
    return findAndSelectElement(driver, elementXpath, elementName, "461")


def setApplicantsNumber(driver):
    """"
    set the Number of applicants who need a residence title (inluding foreign spouse and children)
    """
    elementXpath = '//*[@id="xi-sel-422"]'
    elementName = "Applications Count"
    return findAndSelectElement(driver, elementXpath, elementName, "1")


def setFamily(driver):
    elementXpath = '//*[@id="xi-sel-427"]'
    elementName = "Family member"
    return findAndSelectElement(driver, elementXpath, elementName, "2")


def setVisaGroup(driver):
    elementXpath = '//*[@id="xi-div-30"]/div[1]/label/p'
    elementName = "set visa group"
    return findAndClickElement(driver, elementXpath, elementName)


def setVisaType(driver):
    elementXpath = '//*[@id="inner-461-0-1"]/div/div[3]/label'
    elementName = "set visa type"
    return findAndClickElement(driver, elementXpath, elementName)


def setBlueCard(driver):
    elementXpath = '//*[@id="inner-461-0-1"]/div/div[4]/div/div[1]/label'
    elementName = "click blue card"
    return findAndClickElement(driver, elementXpath, elementName)


def setQualifiedSkilledWithAE(driver):
    # Click to Book appointment
    elementXpath = '//*[@id="SERVICEWAHL_EN163-0-1-1-329328"]'
    elementName = "qualifiedSkilled"
    return findAndClickElement(driver, elementXpath, elementName)


def clickNext(driver):
    elementXpath = '//*[@id="applicationForm:managedForm:proceed"]'
    elementName = "next button"
    return findAndClickElement(driver, elementXpath, elementName)


def handleError(driver):
    # Check Error Message
    pageTimer = 0
    elementXpath = '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div/div[1]/div[3]/div[1]/fieldset/legend'
    while(1):
        try:
            if(driver.find_element_by_class_name("errorMessage")):
                myLogger.info(
                    f"No appointment, starting to process again in {TIMEOUT} seconds ...")
                time.sleep(TIMEOUT)
                return False
            if(pageTimer > PAGE_TIMEOUT):
                myLogger.info("Failed to load the page withim limit")
                return False
            else:
                sourceHtml = driver.page_source
                f = open("source-"+str(randint(1,100))+".html","w")
                f.write(sourceHtml)
                f.close()
                myLogger.info("FOUND IT")
                return True
        except(NoSuchElementException, ElementNotInteractableException):
            myLogger.info("Page is loading")
        except(UnexpectedAlertPresentException):
            myLogger.warn("Someproblem happend ")
            return True
        except(WebDriverException):    
           myLogger("Error on finding the driver")
           pass

        time.sleep(1)
        pageTimer += 1


def setDriver():
    op = webdriver.ChromeOptions()
    #op.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="./driver/win32/chromedriver",options=op)

    return driver


if __name__ == "__main__":

    driver = setDriver()
    while(1):
        driver.close()
        driver = setDriver()

        if(not getHomePage(driver)):
            continue
        if(not clickBookAppointmentButton(driver)):
            continue
        if(not clickAcceptTermsCheckbox(driver)):
            continue
        if(not clickAcceptTermsButton(driver)):
            continue

        if(not setCitizenship(driver)):
            continue
        if(not setApplicantsNumber(driver)):
            continue
        if(not setFamily(driver)):
            continue

        if(not setVisaGroup(driver)):
            continue
        if(not setVisaType(driver)):
            continue

        if(not setBlueCard(driver)):
            continue

        if(not clickNext(driver)):
            continue

        if(not handleError(driver)):
            continue

        time.sleep(TIMEOUT)

# To do
# After selecting make sure it is done by reading back again the value citizenship example sometimes doesn't select Turkey. Repeat it until is succeeds.