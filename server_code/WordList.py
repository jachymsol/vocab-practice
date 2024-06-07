import random
import anvil.server
import anvil.users
from anvil.tables import app_tables

def get_practice_word():
    words = app_tables.words.search(guid=anvil.users.get_user().get_id())
    return random.choice(words)['word']

def add_word(word):
    app_tables.words.add_row(
        guid=anvil.users.get_user().get_id(),
        word=word,
        language='de'
    )

def get_list():
    return app_tables.words.search(
        guid=anvil.users.get_user().get_id(), 
        language='de'
    )

def delete_word(word):
    app_tables.words.search(
        guid=anvil.users.get_user()['guid'],
        language='de',
        word=word
    )[0].delete()
