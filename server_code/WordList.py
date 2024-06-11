import random
import anvil.users
import anvil.tables.query as q
from anvil.tables import app_tables


def get_practice_word(user=None):
    if not user:
        user = anvil.users.get_user()

    words = app_tables.words.search(
        guid=user['guid'],
        language='de',
        learned=False
    )
    if len(words) == 0:
        return None
    word_to_practice = random.choices(words, weights=[100 - word['confidence'] for word in words], k=1)[0]
    return word_to_practice['word']


def add_word(word, user=None):
    if not user:
        user = anvil.users.get_user()
    
    word_in_list = app_tables.words.search(
        guid=user['guid'],
        language='de',
        word=q.ilike(word)
    )
    if len(word_in_list) > 0:
        return {'error': f'Word {word} is already in your list.'}

    app_tables.words.add_row(
        guid=user['guid'],
        word=word,
        language='de',
        n_practiced=0,
        learned=False,
        confidence=50
    )
    return {}


def increment_word_practiced(word, user=None):
    if not user:
        user = anvil.users.get_user()
    
    app_tables.words.get(
        guid=user['guid'],
        language='de',
        word=word
    )['n_practiced'] += 1
    return {}


def set_word_learned(word, learned, user=None):
    if not user:
        user = anvil.users.get_user()
    
    app_tables.words.get(
        guid=user['guid'],
        language='de',
        word=word
    )['learned'] = learned
    return {}


def set_word_confidence(word, confidence, user=None):
    if not user:
        user = anvil.users.get_user()
    
    app_tables.words.get(
        guid=user['guid'],
        language='de',
        word=word
    )['confidence'] = confidence
    return {}


def get_list(pattern="", user=None):
    if not user:
        user = anvil.users.get_user()
    
    return app_tables.words.search(
        guid=user['guid'],
        language='de',
        word=q.ilike(f"%{pattern}%")
    )


def delete_word(word, user=None):
    if not user:
        user = anvil.users.get_user()
    
    app_tables.words.get(
        guid=user['guid'],
        language='de',
        word=word
    ).delete()
    return {}
