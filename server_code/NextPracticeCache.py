import OpenAI as AI
import WordList
import anvil.users
from anvil.tables import app_tables

def refresh_next_practice_cache(user, force=False):
    practice = app_tables.cached_practice.get(guid=user['guid'], language='de')
    if practice and not force and validate_cached_practice(practice):
        return {}
    
    word = WordList.get_practice_word(user=user)
    examples = AI.get_examples('de', word, 3)
    translation = AI.get_translation('de', word)

    if "error" in examples or "error" in translation:
        raise Exception(f"Error getting practice lesson: {examples['error'] if 'error' in examples else translation['error']}")

    save_cached_practice(user, word, examples.get('examples', []), translation.get('translation', ""), practice)

def save_cached_practice(user, word, examples, translation, existing_row=None):
    if existing_row:
        existing_row.update(
            next_word=word,
            next_examples=examples,
            next_translation=translation,
            next_invalidated=False
        )
    else:
        app_tables.cached_practice.add_row(
            guid=user['guid'],
            language='de',
            next_word=word,
            next_examples=examples,
            next_translation=translation,
            next_invalidated=False
        )

def get_cached_practice(user=None):
    if not user:
        user = anvil.users.get_user()
    if user == None:
        return {"error": "User not logged in."}
    
    practice = app_tables.cached_practice.get(guid=user['guid'], language='de')
    if practice == None or not validate_cached_practice(practice):
        return {}
    
    return practice

def invalidate_cached_practice(user=None):
    if not user:
        user = anvil.users.get_user()
    if user == None:
        return {"error": "User not logged in."}
    
    practice = app_tables.cached_practice.get(guid=user['guid'], language='de')
    if practice == None:
        return {}
    practice['next_invalidated'] = True

def validate_cached_practice(practice):
    if not practice:
        return False

    if practice['next_invalidated']:
        return False
    
    word = app_tables.words.get(guid=practice['guid'], language='de', word=practice['next_word'])
    if not word:
        return False
    
    if word['learned']:
        return False
    
    return True