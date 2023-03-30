import math
import jwt
import time
import datetime
import random
from _thread import start_new_thread
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chromium.service import ChromiumService

from django.conf import settings

df = pd.read_excel('name.xlsx')
options = ChromiumOptions()
options.add_argument('--headless')
options.add_argument("use-fake-ui-for-media-stream")
options.add_argument("--use-fake-device-for-media-stream")
desired_cap = {
    'chromeOptions': {
        'args': ["--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream"]
    }
}
ser = ChromiumService('chromedriver.exe', start_error_message="HELL")

ROLE = 0
CHINA = 0
LANG = 'en-US'
SDK_KEY = settings.CLIENT_ID
API_SECRET = settings.CLIENT_SECRET
STORE_BROWSER_DICT = dict()

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

    browser = webdriver.Chrome(
        executable_path='chromedriver.exe', service=ser, options=options, desired_capabilities=desired_cap)
    browser.get(url)
    start_new_thread(click_button, (browser,))
    if meeting_id in STORE_BROWSER_DICT:
        STORE_BROWSER_DICT[meeting_id] = STORE_BROWSER_DICT[meeting_id].append(browser)
    else:
        STORE_BROWSER_DICT[meeting_id] = [browser]
    return browser


def add_participants(meeting_code, meeting_password, no_of_participants):
    signature = generate_sdk_signature(meeting_code)    
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
        print(start_new_thread(get_browser, ("http://127.0.0.1:9999/meeting.html?"+comb, meeting_code,)))

def remove_meeting(meeting_code):
    if meeting_code in STORE_BROWSER_DICT:
        for meeting_browser in STORE_BROWSER_DICT[meeting_code]:
            try:
                meeting_browser.quit()
            except Exception as ex:
                print(ex)
        del STORE_BROWSER_DICT[meeting_code]





# Meeting ID: 7835046932
# Passcode: 8jjSj0
# //*[@id="voip-tab"]/div/button

