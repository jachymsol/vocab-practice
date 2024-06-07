from ._anvil_designer import PracticeFormTemplate
from anvil import *
import anvil.server
import anvil.users


class PracticeForm(PracticeFormTemplate):
  def __init__(self, **properties):
    # Set Item properties
    self.item['practice_word'] = None
    self.item['practice_examples'] = None
    self.item['practice_translation'] = None
    self.item['practice_translation_visible'] = None

    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def show_next_practice(self):
    self.item['practice_word'], self.item['practice_examples'], self.item['practice_translation'] = anvil.server.call('get_practice_lesson')
    self.item['practice_translation_visible'] = False
    self.refresh_data_bindings()

  def start_practice_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if anvil.users.get_user() == None:
      anvil.ErrorAlert("You must be logged in to start practicing").show()
    self.show_next_practice()

  def show_practice_translation_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.item['practice_translation_visible'] = True
    self.refresh_data_bindings()

  def next_practice_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.show_next_practice()

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
    anvil.server.call('add_word_to_list', self.word_input.text)
    anvil.Notification("Word added successfully").show()
    self.word_input.text = ""
    self.single_word_info.visible = False
    self.refresh_data_bindings()
