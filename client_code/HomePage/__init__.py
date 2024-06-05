from ._anvil_designer import HomePageTemplate
import anvil.server
import anvil.users


class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    self.item['practice_word'] = None
    self.item['practice_translation'] = None
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    if not anvil.users.get_user():
      self.start_practice_button.enabled = False
      self.start_practice_button.text = "Log-in to Practice"
    # Any code you write here will run before the form opens.

  def start_practice_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.item['practice_word'] = anvil.server.call('get_practice_word')
    self.item['practice_translation'] = None
    self.practice_sentences.text = anvil.server.call('get_examples', word=self.item['practice_word'])
    self.refresh_data_bindings()

  def show_practice_translation_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.item['practice_translation'] = anvil.server.call('get_translation', self.item['practice_word'])
    self.refresh_data_bindings()

  def next_practice_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.item['practice_word'] = anvil.server.call('get_practice_word')
    self.item['practice_translation'] = None
    self.practice_sentences.text = anvil.server.call('get_examples', word=self.item['practice_word'])
    self.refresh_data_bindings()

  def view_translation_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.single_word_info.text = anvil.server.call('get_translation', self.word_input.text)
    self.single_word_info.visible = True

  def view_word_examples_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.single_word_info.text = anvil.server.call('get_examples', self.word_input.text)
    self.single_word_info.visible = True
