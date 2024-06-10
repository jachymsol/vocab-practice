from ._anvil_designer import WordListFormTemplate # type: ignore
import anvil.server


class WordListForm(WordListFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.word_row.set_event_handler('x-refresh-words', self.refresh_words)
    
    if anvil.users.get_user() == None:
      anvil.Notification("You must be logged in to save and view words", style="warning").show()
      return
    self.refresh_words()

  def refresh_words(self, **event_args):
    words_list = anvil.server.call('get_words_list')
    self.word_row.items = [{'word': word['word'], 'n_practiced': word['n_practiced'], 'learned': word['learned'], 'confidence': word['confidence']} for word in words_list]
