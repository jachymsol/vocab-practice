from ._anvil_designer import HomePageTemplate # type: ignore
from anvil_extras import routing # type: ignore
import PracticeForm, WordListForm, ErrorForm
import anvil.server
import anvil.users


@routing.default_template
class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    routing.set_url_hash('')

    # Any code you write here will run before the form opens.
    user = anvil.users.get_user()
    if user:
      anvil.server.call('refresh_next_practice_cache', False)
      self.show_logged_in(user)

  def login_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.login_with_form(allow_cancel=True)
    user = anvil.users.get_user()
    if user:
      if user['guid'] == None:
        anvil.server.call('generate_guid', user.get_id())
      with anvil.server.no_loading_indicator:
        anvil.server.call('refresh_next_practice_cache', False)
      self.show_logged_in(user)
  
  def logout_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    self.logged_email.text = ""
    self.login_button.text = "Login"
    self.login_button.set_event_handler('click', self.login_button_click)
    self.refresh_data_bindings()

  def show_logged_in(self, user):
    self.logged_email.text = user['email']
    self.login_button.text = "Logout"
    self.login_button.set_event_handler('click', self.logout_button_click)
    self.refresh_data_bindings()

  def title_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.open_form('HomePage')

  def home_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    routing.set_url_hash('')

  def word_list_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    routing.set_url_hash('words')
