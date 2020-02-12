################################################################
### main.py
################################################################

#usage: python3 main.py USERNAME B64_PASSWORD ROOM(e.g. S314) BACKUP_ROOM START_TIME END_TIME

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from base64 import b64decode
from discord_webhook import DiscordWebhook, DiscordEmbed
import sys

# Variables
BYGG_DICT = {'S': 'Smaragd',
             'K': 'Kobolt',
             'G': 'Gneis',
             'A': 'Ametyst'}

USER = sys.argv[1]
ROOM = sys.argv[3]
BYGG = BYGG_DICT[ROOM[0]]

BACKUP_ROOM = sys.argv[4]
BACKUP_BYGG = BYGG_DICT[BACKUP_ROOM[0]]

PWD = str(b64decode(sys.argv[2]), 'utf-8')

TIME1 = sys.argv[5] #start time
TIME2 = sys.argv[6] #end time

#format: 'HH:MM'

WEBHOOK = DiscordWebhook(
    url='https://discordapp.com/api/webhooks/676700802001272838/NGKja4yUeqWUYyg-DN85VhQQZJzEHP1h0bONRyBvFycXVeATL4_OsDuH4T6HiNAsmwi8')

URL = 'https://tp.uio.no/ntnu/rombestilling/'

# Options for Chrome
CHROME_PATH = '/usr/bin/google-chrome' # May be different
CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH


def notify_webhook(is_backup, start, end, date):
    color = 242424

    if is_backup:
        message = f'{ROOM} er ikke ledig {start}-{end}, {date}. Booker {BACKUP_ROOM}.'
        color = 118811
    else:
        message = f'{ROOM} eller {BACKUP_ROOM} er ikke ledig {start}-{end}, {date}. Bruker: {USER}.'

    embed = DiscordEmbed(title='Rom utilgjengelig',
                         description=message, color=color)
    WEBHOOK.add_embed(embed)
    WEBHOOK.execute()



def book_room():
    # Initiate driver for Chrome
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              options=chrome_options)
    driver.implicitly_wait(20)                          

    # Go to the web page
    driver.get(URL)

    # Choose organization
    driver.find_element_by_xpath(
        "//input[@id='org_selector-selectized']").click()
    driver.find_element_by_xpath("//div[@data-value='ntnu.no']").click()
    driver.find_element_by_id('selectorg_button').click()

    # Log in
    login_username = driver.find_element_by_id('username')
    login_username.send_keys(USER)
    login_password = driver.find_element_by_id('password')
    login_password.send_keys(PWD)
    driver.find_element_by_xpath("//button").click()

    # Select start time and end time
    start = Select(driver.find_element_by_id('start'))
    start.select_by_visible_text(TIME1)
    duration = Select(driver.find_element_by_id('duration'))
    duration.select_by_visible_text(TIME2)

    # Calculate 14 days in the future and set the date
    deltadate = datetime.today() + timedelta(days=14)
    day = deltadate.strftime('%d')
    month = deltadate.strftime('%m')
    year = deltadate.strftime('%Y')
    date = deltadate.strftime('%d.%m.%y')

    # Set the date
    input_date = driver.find_element_by_id("preset_date")
    driver.execute_script(
        f'arguments[0].setAttribute("value","{day}.{month}.{year}");',
        input_date)

    # Select desired area and building
    area = Select(driver.find_element_by_id('area'))
    area.select_by_visible_text('Gjøvik')
    building = Select(driver.find_element_by_id('building'))
    building.select_by_visible_text(BYGG)
    size = driver.find_element_by_id("size")
    driver.execute_script(f'arguments[0].setAttribute("value","2");', size)
    size.submit()

    bygg = ''
    room = ''

    # Send notification if the room is unavailable
    if f'{BYGG} {ROOM}' in driver.page_source:
        bygg = BYGG
        room = ROOM
    elif f'{BACKUP_BYGG} {BACKUP_ROOM}' in driver.page_source:
        bygg = BACKUP_BYGG
        room = BACKUP_ROOM
        notify_webhook(True, TIME1, TIME2, date)
    else:
        notify_webhook(False, TIME1, TIME2, date)
        driver.close()
        return

    # Check the desired room
    driver.find_element_by_xpath(
        f"// tr[td/a/text()[contains(., '{bygg} {room}')]]/td[@title='Velg']/input").click()

    # Confirm order
    driver.find_element_by_id("rb-bestill").click()
    driver.find_element_by_xpath(
        "//input[contains(@value, 'Bekreft')]").click()
    driver.find_element_by_xpath(
        "//input[contains(@value, 'samme kriterier')]").click()

    # Close the driver
    driver.close()


if __name__ == '__main__':
    book_room()
