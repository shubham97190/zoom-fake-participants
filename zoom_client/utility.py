import math
import jwt
import time
import datetime
import random
from _thread import start_new_thread
import pandas as pd
import subprocess
from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chromium.service import ChromiumService

from django.conf import settings

df = pd.read_excel('name.xlsx')
options = ChromiumOptions()
options.add_argument('--headless')
options.add_argument("use-fake-ui-for-media-stream")
options.add_argument("--use-fake-device-for-media-stream")
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")

options.add_argument("--remote-debugging-port=9222")  # this

options.add_argument("--disable-dev-shm-using")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
desired_cap = {
    'options': {
        'args': ["--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream"]
    }
}
# ser = ChromiumService('chromedriver.exe', start_error_message="HELL")

ROLE = 0
CHINA = 0
LANG = 'en-US'
SDK_KEY = settings.CLIENT_ID
API_SECRET = settings.CLIENT_SECRET
STORE_BROWSER_DICT = dict()
MEETING_URL = 'http://101.53.148.83:9999/meeting.html'
def click_button(browser):
    try:
        time.sleep(5)
        participants_button = browser.find_element_by_xpath('//*[@id= "voip-tab"]/div/button')
        participants_button.click()
        return
    except:
        click_button(browser)


def generate_sdk_signature(meeting_number):
    iat = math.floor(datetime.datetime.now().timestamp()) - 30
    exp = iat + 60 * 60 * 2

    signature = jwt.encode(

        # Create a payload of the token containing
        # API Key & expiration time
        {'sdkKey': SDK_KEY, 'mn': meeting_number, 'role': ROLE, 'iat': iat,
            'exp': exp, 'appKey': SDK_KEY, 'tokenExp': iat + 60 * 60 * 2},

        # Secret used to generate token signature
        API_SECRET,

        # Specify the hashing alg
        algorithm='HS256'
    )
    # print(signature)
    return signature


def _combine_to_string(data: dict) -> str:
    return "&".join(["=".join([str(k), str(v)]) for k, v in data.items()])


def get_browser(url, meeting_id):

    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    start_new_thread(click_button, (browser,))
    if meeting_id in STORE_BROWSER_DICT:
        brow = STORE_BROWSER_DICT[meeting_id]
        STORE_BROWSER_DICT[meeting_id] = brow +[browser]
    else:
        STORE_BROWSER_DICT[meeting_id] = [browser]
    return browser


def add_participants(meeting_code, meeting_password, no_of_participants):
    signature = generate_sdk_signature(meeting_code) 
    url_link_list = []   
    for name in random.sample(df['name'].tolist(), int(no_of_participants)):
        data = {
            "name": str(name).replace('\xa0',''),
            "mn": meeting_code,
            "email": '',
            "pwd": meeting_password,
            "signature": signature,
            "sdkKey": SDK_KEY,
            "china": CHINA,
            "lang": LANG,
            "role": ROLE
        }
        comb = _combine_to_string(data)
        url_link_list.append(f"{MEETING_URL}?{comb}")

    urls_string = ",".join(url_link_list)
    process = subprocess.Popen(["python", "sele_the.py", "--urls", urls_string])
    if meeting_code in STORE_BROWSER_DICT:
        brow = STORE_BROWSER_DICT[meeting_code]
        STORE_BROWSER_DICT[meeting_code] = brow +[process]
    else:
        STORE_BROWSER_DICT[meeting_code] = [process]

def remove_meeting(meeting_code):
    if meeting_code in STORE_BROWSER_DICT:
        for meeting_browser in STORE_BROWSER_DICT[meeting_code]:
            try:
                if meeting_browser.poll() is not None:
                    print("Subprocess terminated gracefully with return code:", meeting_browser.returncode)
                else:
                    # If the subprocess did not terminate gracefully, force kill it
                    meeting_browser.kill()
                    print("Subprocess forcefully killed")
            except Exception as ex:
                print(ex)
        if meeting_code in STORE_BROWSER_DICT:del STORE_BROWSER_DICT[meeting_code]





# Meeting ID: 7835046932
# Passcode: 8jjSj0
# //*[@id="voip-tab"]/div/button

