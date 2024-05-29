from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.server


class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    self.item['practice_word'] = None
    self.item['practice_translation'] = None
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def start_practice_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.practice_sentences.text = anvil.server.call('get_pracice_examples')
    self.item['practice_word'] = "Tisch"
    self.item['practice_translation'] = None
    self.refresh_data_bindings()

  def show_practice_translation_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.item['practice_translation'] = "Table"
    self.refresh_data_bindings()

  def next_practice_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.item['practice_translation'] = None
    self.refresh_data_bindings()

  def view_translation_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.single_word_info.text = anvil.server.call('get_translation', self.word_input.text)
    self.single_word_info.visible = True

  def view_word_examples_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.single_word_info.text = anvil.server.call('get_examples', self.word_input.text)
    self.single_word_info.visible = True
