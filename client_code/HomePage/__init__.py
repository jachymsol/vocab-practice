from ._anvil_designer import HomePageTemplate
import anvil.server
import anvil.users
from anvil import Notification


class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    self.item['practice_word'] = None
    self.item['practice_translation'] = None
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

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
  
  def add_word_to_list_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('add_word', self.word_input.text)
    anvil.Notification("Word added successfully").show()
    self.word_input.text = ""
    self.single_word_info.visible = False

  def login_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.login_with_form(allow_cancel=True)
    self.login_button.enabled = False
    self.login_button.text = "Logged-In"
    self.item['logged_in'] = True
    self.refresh_data_bindings()
