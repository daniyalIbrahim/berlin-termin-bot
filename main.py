
import time
import threading
from models.scraper import TerminScraper
from models.page import ScraperPage

links = ["https://otv.verwalt-berlin.de/ams/TerminBuchen"]

list_xpaths_to_click = [
    '//*[@id="mainForm"]/div/div/div/div/div/div/div/div/div/div[1]/div[1]/div[2]/a',
    '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[4]/div[1]/div[4]/input',
    '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[5]/button',
    '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[9]/div[1]/div[1]/div[1]/div[1]/label',
    '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[9]/div[1]/div[1]/div[1]/div[6]/div/div[4]/div/div[11]/input'
]
list_xpaths_to_click_scroll = [
    '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[9]/div[1]/div[1]/div[1]/div[6]/div/div[3]/label',
    '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[5]/button'
]
list_xpaths_to_select = [
    '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[2]/select',
    '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[3]/div[1]/div[1]/select',
    '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[4]/select'
]
list_xpaths_to_select_scroll = [
]
list_select_options = ["Pakistan", "eine Person", "nein"]


def run_multi_threaded():
    start_time = time.time()
    threads = []
    for link in links:  # each thread could be like a new 'click'
        scraper = TerminScraper(url=link)
        th = threading.Thread(target=scraper.apply)
        th.start()  # could `time.sleep` between 'clicks' to see whats'up without headless option
        threads.append(th)
    for th in threads:
        th.join()  # Main thread wait for threads finish
    print("multiple threads took ", (time.time() - start_time), " seconds")


def run_sequential():
    start_time = time.time()
    landing_page = ScraperPage(name="landing_page", list_xpaths_to_click=[
                        '//*[@id="mainForm"]/div/div/div/div/div/div/div/div/div/div[1]/div[1]/div[2]/a'])
    information_page = ScraperPage(name="information_page",
                            list_xpaths_to_click=['/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[4]/div[1]/div[4]/input',
                                                  '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[5]/button'])
    service_page = ScraperPage(name="service_page",
                        list_xpaths_to_click=[
                            '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[9]/div[1]/div[1]/div[1]/div[1]/label',  
                            '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[9]/div[1]/div[1]/div[1]/div[6]/div/div[4]/div/div[11]/input'],
                        list_xpaths_to_click_scroll=['/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[9]/div[1]/div[1]/div[1]/div[6]/div/div[3]/input',
                                                     '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[5]/button'],
                        list_xpaths_to_select=['/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[2]/select',
                                               '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[3]/div[1]/div[1]/select',
                                               '/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div[8]/div[1]/div[2]/div[1]/fieldset/div[4]/select'],
                        list_select_options=["Pakistan", "eine Person", "nein"])
    scraper = TerminScraper(url=links[0], landing_page=landing_page,
                            information_page=information_page, service_page=service_page)
    scraper.apply()
    print("sequential took ", (time.time() - start_time), " seconds")


def main():
    # run_multi_threaded()
    run_sequential()


if __name__ == '__main__':
    main()
