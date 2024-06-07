from ._anvil_designer import WordListFormTemplate
from anvil import Button
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class WordListForm(WordListFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    words_list = anvil.server.call('get_words_list')
    self.words_table.items = [{'word': word['word'], 'n_practiced': word['n_practiced'], 'learned': word['learned'], 'confidence': word['confidence'], 'remove': RemoveButton(word='word')} for word in words_list]


class RemoveButton(Button):
  def __init__(self, word, **properties):
    self.word = word
    super().__init__(text='', icon='fa:trash', **properties)
