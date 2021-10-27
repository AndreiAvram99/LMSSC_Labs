# Import packages
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# Extract text
source = urlopen('https://ro.wikipedia.org/wiki/Mihai_Eminescu').read()
soup = BeautifulSoup(source, features='html.parser')
text = ''
for paragraph in soup.find_all('p'):
    text += paragraph.text

# Save text into file
file = open("corpus.txt", "w", encoding="utf-8")
file.write(text)

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
url_regex = r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
ip_address = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'


def check_email(word):
    if re.fullmatch(email_regex, word):
        return True
    return False


def check_url(word):
    if re.fullmatch(url_regex, word):
        return True
    return False


def check_ip_address(word):
    if re.fullmatch(ip_address, word):
        return True
    return False


def check_polite_pronoun(word:str):
    if word.lower() == "dr." \
            or word.lower() == "dna." \
            or word.lower() == "dvs." \
            or word.lower() == "dv."\
            or word.lower() == "dl.":
        return True
    return False


def start_with_big_letter(word:str):
    if word[0].isupper():
        return True
    return False


def parse_punctuation_marks_before(word: str):
    for i in range(len(word)):
        if word[i].isalpha():
            return word[i:]
        else:
            print(word[i])


# text = "Dl. Mihai Eminescu. Merge sasa asasa"
words_list = text.split(' ')

# for i in range(len(words_list)):
    # token = ''
    # crt_word = words_list[i]
    #
    # if check_email(crt_word):
    #     print(crt_word)
    #
    # if check_ip_address(crt_word):
    #     print(crt_word)
    #
    # if check_polite_pronoun(crt_word):
    #     token += crt_word
    #     while start_with_big_letter(words_list[i+1]):
    #         token += ' ' + words_list[i+1]
    #         i += 1
    #     crt_word = words_list[i]
    #     print(token)
    #
    # if start_with_big_letter(crt_word):
    #     while start_with_big_letter(words_list[i+1]):
    #         token += ' ' + words_list[i + 1]
    #         i += 1
    #     crt_word = words_list[i]
    #     print(token)
