import selenium
import time
import sys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

browser = 'firefox'
if len(sys.argv) == 2:
    browser = sys.argv[1]
if browser.lower() == 'firefox':
    driver = selenium.webdriver.Firefox()
elif browser.lower() == 'chrome':
    driver = selenium.webdriver.Chrome()
else:
    print(f'unsupported browser called: {browser}')
    print(f'contact me at github or open an issue to get {browser} support')
    sys.exit(1)
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
    is_valid = True
    for bad_char in bad_letters:
        if bad_char in each:
            is_valid = False
            break
    if is_valid and middle_letter in each:
        good_words.append(each)

# find enter button
enter_button = driver.find_element(By.CLASS_NAME, 'hive-action__submit')

for word in good_words:
    for char in word:
        time.sleep(.5)
        btns[char].click()    
    print('end inner loop')
    time.sleep(1)
    enter_button.click()
    driver.execute_script("arguments[0].click();", enter_button)
