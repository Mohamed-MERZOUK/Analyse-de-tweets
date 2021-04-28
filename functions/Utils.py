from functions.NLP import tokenize_lowercase

import secrets

def get_tags(text):
    return tokenize_lowercase(text)

def get_random_element(liste_element=["primary","secondary","success",'danger',"info","warning",'dark']):
    return secrets.choice(liste_element)
