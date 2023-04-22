import requests
from bs4 import BeautifulSoup
import re
import sys
header = {'User-Agent': 'Mozilla/5.0'}
language_key = {
    1: 'Arabic',
    2: 'German',
    3: 'English',
    4: 'Spanish',
    5: 'French',
    6: 'Hebrew',
    7: 'Japanese',
    8: 'Dutch',
    9: 'Polish',
    10: 'Portuguese',
    11: 'Romanian',
    12: 'Russian',
    13: 'Turkish'
}
args = sys.argv
lang, translate, word = args[1], args[2], args[3]
if translate.capitalize() not in language_key.values() and translate != "all":
    print(f"Sorry, the program doesn't support {translate}")
    quit()
s = requests.Session()
counter = 0
to_save = ""
if translate == "all":
    for help_lang in language_key.values():
        if help_lang == lang.capitalize():
            continue
        else:
            r = requests.get(
                f'https://context.reverso.net/translation/{lang}-{help_lang.lower()}/{word}',
                headers=header)
            if r:
                soup = BeautifulSoup(r.content, 'html.parser')
                words = []
                words.extend([x.text.strip() for x in soup.select("#translations-content > .translation")])
                sentences = [x.text.strip() for x in soup.select("#examples-content > .example >  .ltr")]
                to_save += f'\n{help_lang} Translations:\n'
                to_save += f"{re.sub(r' ..?$', '', words[0])}\n"
                to_save += f'\n{help_lang} Example:\n'
                to_save += f"{sentences[0]}:\n"
                to_save += f"{sentences[1]}\n"
            elif r.status_code == 404:
                print(f"Sorry, unable to find {word}")
                quit()
            else:
                print("Something went wrong with your internet connection")
                quit()
else:
    r = requests.get(f'https://context.reverso.net/translation/{lang}-{translate.lower()}/{word}', headers=header)
    if r:
        soup = BeautifulSoup(r.content, 'html.parser')
        words = []
        words.extend([x.text.strip() for x in soup.select("#translations-content > .translation")])
        sentences = [x.text.strip() for x in soup.select("#examples-content > .example >  .ltr")]
        to_save += f'\n{translate.capitalize()} Translations:\n'
        to_save += f"{re.sub(r' ..?$', '', words[0])}\n"
        to_save += f'\n{translate.capitalize()} Example:\n'
        to_save += f"{sentences[0]}:\n"
        to_save += f"{sentences[1]}\n"
    elif r.status_code == 404:
        print(f"Sorry, unable to find {word}")
        quit()
    else:
        print("Something went wrong with your internet connection")
        quit()
with open(f'{word}.txt', 'w') as file:
    file.write(to_save)
    print(to_save)
