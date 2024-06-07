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

    if examples.error or translation.error:
        return {"error": f"Error getting practice lesson: {examples.error if examples.error else translation.error}"}
    return {
        "error": None, 
        "word": word,
        "exists": examples.exists and translation.exists,
        "examples": examples.examples, 
        "translation": translation.translation
    }

@anvil.server.callable
def get_translation(word):
    translation = AI.get_translation('de', word)
    if translation.error:
        return {"error": f"Error getting translation: {translation.error}"}
    return {
        "error": None,
        "exists": translation.exists,
        "translation": translation.translation
    }

@anvil.server.callable
def get_examples(word):
    examples = AI.get_examples('de', word, 5)
    if examples.error:
        return {"error": f"Error getting examples: {examples.error}"}
    return {
        "error": None,
        "exists": examples.exists,
        "examples": examples.examples
    }

@anvil.server.callable
def get_words_list():
    return WordList.get_list()

@anvil.server.callable
def add_word_to_list(word):
    WordList.add_word(word)
    return {"error": None}

@anvil.server.callable
def delete_word(word):
    WordList.delete_word(word)