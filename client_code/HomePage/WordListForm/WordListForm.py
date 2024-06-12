from ._anvil_designer import WordListFormTemplate # type: ignore
from anvil.js.window import document # type: ignore
from anvil_extras import routing # type: ignore
import anvil.server


@routing.route('words')
class WordListForm(WordListFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    document.addEventListener('keyup', self.global_keyboard_shortcuts)
    self.word_row.set_event_handler('x-refresh-words', self.refresh_words)
    
    if anvil.users.get_user() == None:
      anvil.Notification("You must be logged in to save and view words", style="warning").show()
      return
    self.refresh_words()

  def refresh_words(self, **event_args):
    words_list = anvil.server.call('search_words_list', self.search_box.text)
    self.word_row.items = [{'word': word['word'], 'n_practiced': word['n_practiced'], 'learned': word['learned'], 'confidence': word['confidence']} for word in words_list]

  def global_keyboard_shortcuts(self, event):
    if event.key == '/':
      self.search_box.focus()
