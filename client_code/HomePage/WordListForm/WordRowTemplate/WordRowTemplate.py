from ._anvil_designer import WordRowTemplateTemplate
import anvil.server
import anvil.users
from anvil.tables import app_tables


class WordRowTemplate(WordRowTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def remove_word_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if anvil.confirm(f"Do you wish to delete word {self.item['word']}?"):
      anvil.server.call('delete_word', self.item['word'])
      anvil.Notification(f"Word {self.item['word']} deleted successfully").show()
      self.remove_from_parent()
