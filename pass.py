# password generator, for CTFs and/or education
# creates word list, illustrates the large size of possible passwords
# also shows the difficulty of brute force attacks against random passwords

# for illustration/educational use ONLY! These passwords should NOT be considered secure passwords and
# should never be used in a production environment or even for home use.

from random import choice
word_list = []

#character_set = """\"1234567890-=!@#$%^&*()_+qwertyuiop[]QWERTYUIOP{}asdfghjkl;'ASDFGHJKL:'zxcvbnm,./ZXCVBNM<>?"""
# full set of chars from every key and shift + key

character_set ="1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM?!@#$%*&_.'\""
# small version with more likely chars and dis-allowance of dangerous chars like < , -, / and ;
total_pass = (len(character_set))**10 + (len(character_set))**9 + (len(character_set))**8


def eight_to_ten_characters(chars, current_list):
    word = ''
    c = chars
    for i in chars:
        word = word + (choice(c))
        if len(word) <= 10 and len(word) > 7 and word not in current_list:
            return word
            # will first return all possible 8 char combinations, then 9, then 10

def add_the_word(new, w_list):
    if new not in w_list:
        word_list.append(new)

while len(word_list) <= 20000:
    # test version to generate 20000 "secure" 8 to 10 character passwords
    new_word = (eight_to_ten_characters(character_set, word_list))
    add_the_word(new_word, word_list)
    new_word = new_word.swapcase()
    add_the_word(new_word, word_list)
    new_word = new_word.upper()
    add_the_word(new_word, word_list)
    new_word = new_word.lower()
    add_the_word(new_word, word_list)
    # NGL I wrote this mostly to practice string methods.
    # example output: 'h6?%9xnO', 'H6?%9XNo', 'H6?%9XNO', 'h6?%9xno'

print(word_list)
#  note that this has a low chance of generating actual words with the 20k restraint in place
print(f'\nwithout the 20k restriction this would return {total_pass} passwords')
