from nltk.corpus import wordnet as wn
import random
import nltk

nltk.download('wordnet')
domain = input("Type a domain: ")


def get_synset(domain):
    domain_synset = wn.synset(f'{domain}.n.01')
    return domain_synset


def get_hyponyms(domain):
    domain_synset = get_synset(domain)
    domain_hyponyms = domain_synset.hyponyms()
    index = 0
    for hyponym in domain_hyponyms:
        domain_hyponyms[index] = hyponym.name().split(".")[0]
        index += 1
    return domain_hyponyms


def get_antonym(word):
    antonym_list = []
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            if lemma.antonyms():
                antonym_list.append(lemma.antonyms()[0].name())
    return antonym_list[0]


def get_def(word):
    word_def = wn.synset(f'{word}.n.01').definition()
    return word_def


def get_synonym(word):
    synonym_list = []
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            synonym_list.append(lemma.name().split(".")[0])
    for synonym in synonym_list:
        if synonym != word:
            return synonym


def has_synonysms(word):
    try:
        synonym_list = []
        for synset in wn.synsets(word):
            for lemma in synset.lemmas():
                synonym_list.append(lemma.name())
    except:
        return False

    if len(synonym_list) > 1:
        print(synonym_list, "\n")
        return True
    else:
        return False


def has_antonyms(word):
    try:
        antonym_list = []
        for synset in wn.synsets(word):
            for lemma in synset.lemmas():
                if lemma.antonyms():
                    antonym_list.append(lemma.antonyms()[0].name())
    except:
        return False

    if len(antonym_list) > 0:
        print(antonym_list, "\n")
        return True
    else:
        return False


domain_hyponyms = get_hyponyms(domain)
# print(domain_hyponyms)


words_list = domain_hyponyms
questions_list = []

for word in words_list:
    rnd = random.randint(0, 2)

    if rnd == 0:
        print("Looking for a synonym for: ", word)
    else:
        print("Looking for an antonym for: ", word)

    if rnd == 0 and has_synonysms(word):
        questions_list.append(f"Synonym for {get_synonym(word)}")
    elif rnd == 1 and has_antonyms(word):
        questions_list.append(f"Antonym for {get_antonym(word)}")
    else:
        questions_list.append(get_def(word))

print(words_list)
print(questions_list)

# print(get_hyponyms(domain))

