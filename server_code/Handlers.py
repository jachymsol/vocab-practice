import NextPracticeCache
import OpenAI as AI
import Users
import WordList
import anvil.server


@anvil.server.callable
def generate_guid(user_id):
    Users.generate_guid(user_id)

@anvil.server.callable
def get_practice_lesson():
    user = anvil.users.get_user()
    if not user:
        return {"error": "User not logged in."}

    cached_lesson = NextPracticeCache.get_cached_practice(user=user)
    if cached_lesson:
        WordList.increment_word_practiced(cached_lesson['next_word'], user=user)
        NextPracticeCache.invalidate_cached_practice(user=user)
        anvil.server.launch_background_task('refresh_next_practice_cache_task', user=user, force=True)
        return {
            "word": cached_lesson['next_word'],
            "exists": True,
            "examples": cached_lesson['next_examples'],
            "translation": cached_lesson['next_translation']
        }
    
    word = WordList.get_practice_word()
    if not word:
        return {"error": "No words to practice, add a word."}
    
    examples = AI.get_examples('de', word, 3)

    if "error" in examples:
        return {"error": f"Error getting practice lesson: {examples['error']}"}
    
    WordList.increment_word_practiced(word, user=user)
    anvil.server.launch_background_task('refresh_next_practice_cache_task', user=user, force=True)
    return {
        "word": word,
        "exists": examples.get("exists", False),
        "examples": examples.get("examples", []),
        "translation": examples.get("translation", "")
    }

@anvil.server.callable
def get_translation(word):
    if not word:
        return {"error": "No word provided."}

    translation = AI.get_translation('de', word)
    if "error" in translation:
        return {"error": f"Error getting translation: {translation['error']}"}
    return {
        "exists": translation.get("exists", False),
        "translation": translation.get("translation", "")
    }

@anvil.server.callable
def get_examples(word):
    if not word:
        return {"error": "No word provided."}

    examples = AI.get_examples('de', word, 5)
    if "error" in examples:
        return {"error": f"Error getting examples: {examples['error']}"}
    return {
        "exists": examples.get("exists", False),
        "examples": examples.get("examples", [])
    }

@anvil.server.callable
def refresh_next_practice_cache(force=False):
    user = anvil.users.get_user()
    if user:
        anvil.server.launch_background_task('refresh_next_practice_cache_task', user, force)

@anvil.server.background_task
def refresh_next_practice_cache_task(user, force=False):
    NextPracticeCache.refresh_next_practice_cache(user, force)

@anvil.server.callable
def search_words_list(pattern):
    return WordList.get_list(pattern)

@anvil.server.callable
def add_word_to_list(word):
    res = WordList.add_word(word)
    return res

@anvil.server.callable
def set_word_learned(word, learned):
    res = WordList.set_word_learned(word, learned)
    return res

@anvil.server.callable
def set_word_confidence(word, confidence):
    res = WordList.set_word_confidence(word, confidence)
    return res

@anvil.server.callable
def delete_word(word):
    res = WordList.delete_word(word)
    return res
