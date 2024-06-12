from ._anvil_designer import ErrorFormTemplate # type: ignore
from anvil_extras import routing # type: ignore


@routing.route('error')
@routing.error_form
class ErrorForm(ErrorFormTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        routing.set_url_hash('error')

        # Any code you write here will run before the form opens.

    def home_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        routing.set_url_hash('')
 