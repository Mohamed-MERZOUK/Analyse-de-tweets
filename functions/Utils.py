from functions.NLP import preprocess, tokenize_lowercase

import secrets


def get_tags(text):
    return preprocess(text)


def get_random_element(liste_element=["primary", "secondary", "success", 'danger', "info", "warning", 'dark']):
    return secrets.choice(liste_element)
