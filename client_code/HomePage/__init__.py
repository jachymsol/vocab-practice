from ._anvil_designer import HomePageTemplate
from PracticeForm import PracticeForm
from WordListForm import WordListForm
import anvil.server
import anvil.users
from anvil import Notification


class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.content_panel.add_component(PracticeForm())

    # Any code you write here will run before the form opens.
    if anvil.users.get_user():
      self.show_logged_in()

  def login_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.login_with_form(allow_cancel=True)
    if anvil.users.get_user():
      self.show_logged_in()

  def show_logged_in(self):
    self.login_button.enabled = False
    self.login_button.text = "Logged-In"
    self.refresh_data_bindings()

  def title_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.open_form('HomePage')

  def home_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(PracticeForm())

  def word_list_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(WordListForm())
