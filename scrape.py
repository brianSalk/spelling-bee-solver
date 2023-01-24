# site must be called https://solvethespellingbee.com/
# app that calls api must be solver.py
import selenium
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

driver = selenium.webdriver.Firefox()

url = 'https://www.nytimes.com/puzzles/spelling-bee'
driver.get(url)
btns = driver.find_elements(By.TAG_NAME, 'button')
found = False
for btn in btns:
    if btn.text.lower() == 'play':
        found = True
        driver.execute_script("arguments[0].click();",btn)
if not found:
    print('unable to get todays spelling-bee, please try again')
hive = driver.find_element(By.CLASS_NAME, 'hive')

good_letters = []
middle_letter = driver.find_element(By.XPATH,"//*[@class='cell-letter' or @class='center']")
middle_letter = middle_letter.get_attribute('innerHTML')
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
#input_field = driver.find_element(By.CLASS_NAME, 'sb-hive-input-content')
print(good_words)
