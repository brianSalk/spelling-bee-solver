def get_good_words(bad_letters,words,middle_letter):
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
    return good_words

def get_bad_letters(good_letters):
    bad_letters = []
    for letter in 'qwertyuiopasdfghjklzxcvbnm':
        if letter not in good_letters:
            bad_letters.append(letter)
    return bad_letters
def get_good_letters_and_buttons(driver):
    hive = driver.find_element(By.CLASS_NAME, 'hive')
    good_letters = []
    btns = {}
    for pol in hive.find_elements(By.TAG_NAME, 'svg'):
        btn = pol.find_element(By.CLASS_NAME, 'cell-letter')
        letter = btn.get_attribute('innerHTML')
        btns[letter] = pol
    for cell in hive.find_elements(By.CLASS_NAME, 'cell-letter'):
        good_letters.append(cell.get_attribute('innerHTML'))
