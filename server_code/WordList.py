import random
import anvil.server
import anvil.users
from anvil.tables import app_tables

@anvil.server.callable
def get_practice_word():
    words = app_tables.words.search(guid=anvil.users.get_user().get_id())
    return random.choice(words)['word']

@anvil.server.callable
def add_word(word):
    app_tables.words.add_row(
        guid=anvil.users.get_user().get_id(),
        word=word,
        language='de'
    )
