import selenium
import time
import sys
import argparse
import word_proc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# argparse stuff
parser = argparse.ArgumentParser()
parser.add_argument(
    "--browser",
    help="Browser used to solve spellingbee, default is firefox",
    default="firefox",
)
parser.add_argument(
    "-l", "--login", action="store_true", help="use to manually log in to NYT"
)
parser.add_argument(
    "-v", "--verbose", action="store_true", help="print words that are being tried"
)
parser.add_argument(
    "-S",
    "--no_solve",
    action="store_true",
    help="do not solve, only list words in terminal",
)
args = parser.parse_args()

# validate arguments
if args.browser == "firefox":
    driver = selenium.webdriver.Firefox()
elif args.browser == "chrome":
    driver = selenium.webdriver.Chrome()
else:
    print(f"unsupported browser called: {args.browser}")
    print(f"contact me at github or open an issue to get {args.browser} support")
    sys.exit(1)

if args.login:  # loggin to NYT
    driver.get(
        "https://myaccount.nytimes.com/auth/enter-email?redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fpuzzles%2Fspelling-bee&amp;response_type=cookie&amp;client_id=games&amp;application=crosswords&amp;asset=navigation-bar"
    )
    wait = WebDriverWait(driver, 2_000)
    wait.until(EC.url_to_be("https://www.nytimes.com/?login=email&auth=login-email"))
url = "https://www.nytimes.com/puzzles/spelling-bee"
driver.get(url)
plat_btn = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//button[text() ='Play']"))
)
driver.execute_script("arguments[0].click();", plat_btn)


middle_letter = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (By.XPATH, "//*[@class='cell-letter' or @class='center']")
    )
)
middle_letter = middle_letter.get_attribute("innerHTML")

good_letters, btns = word_proc.get_good_letters_and_buttons(driver)
bad_letters = word_proc.get_bad_letters(good_letters)
# get list of english dictionary words
words = word_proc.get_words()
good_words = word_proc.get_good_words(bad_letters, words, middle_letter)
if args.no_solve:
    print(good_words)
    sys.exit(0)
if args.verbose:
    print(good_words)

    """
element = driver.find_element(By.XPATH,"//div[@class='purr-blocker-card pz-hide-games-app pz-hide-newsreader']")
driver.execute_script("arguments[0].style.visibility='hidden'", element)
    """
# find enter button
enter_button = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "hive-action__submit"))
)
for word in good_words:
    for char in word:
        btns[char].click()
    time.sleep(1)
    enter_button.click()
    driver.execute_script("arguments[0].click();", enter_button)
