import OpenAI as AI
import WordList
import Users
import anvil.server


@anvil.server.callable
def generate_guid(user_id):
    Users.generate_guid(user_id)

@anvil.server.callable
def get_practice_lesson():
    word = WordList.get_practice_word()
    examples = AI.get_examples('de', word, 3)
    translation = AI.get_translation('de', word)

    if "error" in examples or "error" in translation:
        return {"error": f"Error getting practice lesson: {examples['error'] if 'error' in examples else translation['error']}"}
    return {
        "word": word,
        "exists": examples.get("exists", False) and translation.get("exists", False),
        "examples": examples.get("examples", []),
        "translation": translation.get("translation", "")
    }

@anvil.server.callable
def get_translation(word):
    translation = AI.get_translation('de', word)
    if "error" in translation:
        return {"error": f"Error getting translation: {translation['error']}"}
    return {
        "exists": translation.get("exists", False),
        "translation": translation.get("translation", "")
    }

@anvil.server.callable
def get_examples(word):
    examples = AI.get_examples('de', word, 5)
    if "error" in examples:
        return {"error": f"Error getting examples: {examples['error']}"}
    return {
        "exists": examples.get("exists", False),
        "examples": examples.get("examples", [])
    }

@anvil.server.callable
def get_words_list():
    return WordList.get_list()

@anvil.server.callable
def add_word_to_list(word):
    WordList.add_word(word)
    return {}

@anvil.server.callable
def set_word_learned(word, learned):
    WordList.set_word_learned(word, learned)

@anvil.server.callable
def delete_word(word):
    WordList.delete_word(word)