import selenium
import time
import sys
import argparse
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
# argparse stuff
parser = argparse.ArgumentParser()
parser.add_argument("--browser", help="Browser used to solve spellingbee, default is firefox")
parser.add_argument("-l","--login", action='store_true', help='use to manually log in to NYT')
args = parser.parse_args()

# validate arguments 
if not args.browser or args.browser == 'firefox':
    driver = selenium.webdriver.Firefox()
elif args.browser == 'chrome':
    driver = selenium.webdriver.Chrome()
else:
    print(f'unsupported browser called: {args.browser}')
    print(f'contact me at github or open an issue to get {args.browser} support')
    sys.exit(1)

if args.login: # loggin to NYT
    driver.get('https://myaccount.nytimes.com/auth/enter-email?redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fpuzzles%2Fspelling-bee&amp;response_type=cookie&amp;client_id=games&amp;application=crosswords&amp;asset=navigation-bar')
    input('press any button to continue')

    # enter email
url = 'https://www.nytimes.com/puzzles/spelling-bee'
driver.get(url)
time.sleep(7)
btns = driver.find_elements(By.TAG_NAME, 'button')
found = False
for btn in btns:
    if btn.text.lower() == 'play':
        found = True
        driver.execute_script("arguments[0].click();",btn)
        
if not found:
    print('unable to get todays spelling-bee, please try again')
time.sleep(5)
hive = driver.find_element(By.CLASS_NAME, 'hive')

good_letters = []
middle_letter = driver.find_element(By.XPATH,"//*[@class='cell-letter' or @class='center']")
middle_letter = middle_letter.get_attribute('innerHTML')
btns = {}
for pol in hive.find_elements(By.TAG_NAME, 'svg'):
    btn = pol.find_element(By.CLASS_NAME, 'cell-letter')
    letter = btn.get_attribute('innerHTML')
    btns[letter] = pol
for cell in hive.find_elements(By.CLASS_NAME, 'cell-letter'):
    good_letters.append(cell.get_attribute('innerHTML'))


bad_letters = []
for letter in 'qwertyuiopasdfghjklzxcvbnm':
    if letter not in good_letters:
        bad_letters.append(letter)
# get list of english dictionary words
with open('english_no_proper', 'r') as f:
    words = []
    for word in f:
        word = word.replace('\n','')
        words.append(word)

good_words = []
for each in words:
    each = each.lower()
    is_valid = True
    for bad_char in bad_letters:
        if bad_char in each:
            is_valid = False
            break
    if is_valid and middle_letter in each:
        good_words.append(each)
print(good_words)
# find enter button
enter_button = driver.find_element(By.CLASS_NAME, 'hive-action__submit')

for word in good_words:
    for char in word:
        time.sleep(.5)
        btns[char].click()    
    time.sleep(1)
    enter_button.click()
    driver.execute_script("arguments[0].click();", enter_button)
