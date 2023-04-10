import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import threading
import argparse
import pandas as pd


def create_driver():
    """returns a chrome webdriver headless"""
    chromeOptions = webdriver.ChromeOptions()
    # chromeOptions.add_argument("--headless") # make it not visible
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-setuid-sandbox")

    # chromeOptions.add_argument("--remote-debugging-port=9222")  # this

    chromeOptions.add_argument("--disable-dev-shm-using")
    chromeOptions.add_argument("--disable-extensions")
    chromeOptions.add_argument("--disable-gpu")
    chromeOptions.add_argument("start-maximized")
    chromeOptions.add_argument("--headless")
    chromeOptions.add_argument("disable-infobars")
    return webdriver.Chrome(options=chromeOptions)


def try_click_random_link(driver):
    """try to click on a random link on the opened page"""
    try:
        elements = driver.find_elements_by_tag_name("a:link")
        element = elements[
            len(elements) // 3
        ]  # try being more deterministic for threads/process
        element.click()
    except:
        pass


def get_title(url, webdriver=None):
    """get the url html title using BeautifulSoup
    if driver is None uses a new chrome-driver and quit() after
    otherwise uses the driver provided and don't quit() after
    """

    def print_title(driver):
        driver.get(url)
        # [ try_click_random_link(driver) for i in range(8) ] # try to click-walk through 8 pages on random found links
        soup = BeautifulSoup(driver.page_source, "lxml")
        item = soup.find("title")
        print(item.string.strip())

        while True:
            pass

    if webdriver:
        print_title(webdriver)
    else:
        webdriver = create_driver()
        print_title(webdriver)
        # webdriver.quit()

def main_threads(urls):
    start_time = time.time()

    threads = []
    for link in urls:  # each thread a new 'click'
        th = threading.Thread(target=get_title, args=(link,))
        th.start()  # could sleep 1 between 'clicks' with `time.sleep(1)``
        threads.append(th)
    for th in threads:
        th.join()  # Main thread wait for threads finish

    print("hello")

    return time.time() - start_time


def run_nget_times():
    """only for statistical measuraments - using this as a module"""
    return main_threads()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example script to accept a list of URLs")
    parser.add_argument("--urls", type=str, help="List of URLs separated by spaces")
    args = parser.parse_args()
    urls = args.urls
    dfs = pd.read_csv(urls)
    url_list = dfs["urls"].tolist()
    th_time = main_threads(url_list)
    if os.path.exists(urls):
        os.remove(urls)
    else:
        print("The file does not exist") 
    print("multithreads {:0} seconds ---".format(th_time))
