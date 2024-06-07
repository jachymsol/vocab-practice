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
    examples = AI.get_examples(word)
    translation = AI.get_translation(word)
    return word, examples, translation

@anvil.server.callable
def get_translation(word):
    return AI.get_translation(word)

@anvil.server.callable
def get_examples(word):
    return AI.get_examples(word)

@anvil.server.callable
def get_words_list():
    return WordList.get_list()

@anvil.server.callable
def add_word_to_list(word):
    WordList.add_word(word)
    return True

@anvil.server.callable
def delete_word(word):
    WordList.delete_word(word)