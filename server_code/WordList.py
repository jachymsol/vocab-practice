import random
import anvil.users
from anvil.tables import app_tables


def get_practice_word():
    words = app_tables.words.search(
        guid=anvil.users.get_user()['guid'],
        language='de',
        learned=False
    )
    word_to_practice = random.choices(words, weights=[100 - word['confidence'] for word in words], k=1)[0]
    word_to_practice['n_practiced'] += 1
    return word_to_practice['word']


def add_word(word):
    app_tables.words.add_row(
        guid=anvil.users.get_user()['guid'],
        word=word,
        language='de',
        n_practiced=0,
        learned=False,
        confidence=50
    )


def get_list():
    return app_tables.words.search(
        guid=anvil.users.get_user()['guid'],
        language='de'
    )


def delete_word(word):
    app_tables.words.search(
        guid=anvil.users.get_user()['guid'],
        language='de',
        word=word
    )[0].delete()
