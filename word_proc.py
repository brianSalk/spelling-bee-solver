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
