from ._anvil_designer import WordRowTemplateTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class WordRowTemplate(WordRowTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def remove_word_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if confirm(f"Do you wish to delete word {self.item['word']}?"):
      anvil.server.call('delte_word', self.item['word'])
      anvil.Notification(f"Word {self.item['word']} deleted successfully").show()
      self.remove_from_parent()
