from ._anvil_designer import WordListFormTemplate
from anvil import Button
import anvil.server


class WordListForm(WordListFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    words_list = anvil.server.call('get_words_list')
    self.word_row.items = [{'word': word['word'], 'n_practiced': word['n_practiced'], 'learned': word['learned'], 'confidence': word['guid']} for word in words_list]
