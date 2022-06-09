
import time
from models.terminscraper import TerminScraper

links = ["https://otv.verwalt-berlin.de/ams/TerminBuchen?lang=en"]
PAGE_TIMEOUT = 25
TIMEOUT = 15

def run_sequential():
    scraper = TerminScraper(url=links[0], 
                            t_out=TIMEOUT, 
                            p_out=PAGE_TIMEOUT)
    while(1):
        driver = scraper.get_driver()
        if(not scraper.get_home_page()):
            continue
        if(not scraper.click_book_appointment_button()):
            continue
        if(not scraper.click_accept_terms_checkbox()):
            continue
        if(not scraper.click_accept_terms_button()):
            continue

        if(not scraper.set_citizenship()):
            continue
        if(not scraper.set_applicants_number()):
            continue
        if(not scraper.set_family()):
            continue

        if(not scraper.set_visa_group()):
            continue

        if(not scraper.set_visa_type()):
            continue

        if(not scraper.set_blue_card()):
            continue

        if(not scraper.click_next()):
            continue

        if(not scraper.handle_error()):
            continue

        time.sleep(TIMEOUT)
        driver.close()


def main():
    run_sequential()


if __name__ == '__main__':
    main()
