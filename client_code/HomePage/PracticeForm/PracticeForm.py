from ._anvil_designer import PracticeFormTemplate # type: ignore
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
        res = anvil.server.call('get_practice_lesson')
        if res.error:
            anvil.Notification(res.error, style="danger").show()
            return
        if not res.exists:
            anvil.Notification(f"The word {res.word} does not exist.", style="warning").show()
            return
        
        self.item['practice_word'] = res.word
        self.item['practice_examples'] = '\n'.join(res.examples)
        self.item['practice_translation'] = res.translation

        self.item['practice_translation_visible'] = False
        self.refresh_data_bindings()

    def start_practice_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        if anvil.users.get_user() == None:
            anvil.Notification("You must be logged in to start practicing", style="warning").show()
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
        res = anvil.server.call('get_translation', self.word_input.text)
        if res.error:
            anvil.Notification(res.error, style="danger").show()
            return

        if not res.exists:
            self.single_word_info.text = f"The word {self.word_input.text} does not exist."
            self.single_word_info.visible = True

        self.single_word_info.text = res.translation 
        self.single_word_info.visible = True

    def view_word_examples_click(self, **event_args):
        """This method is called when the button is clicked"""
        res = anvil.server.call('get_examples', self.word_input.text)
        if res.error:
            anvil.Notification(res.error, style="danger").show()
            return
        
        if not res.exists:
            self.single_word_info.text = f"The word {self.word_input.text} does not exist."
            self.single_word_info.visible = True

        self.single_word_info.text = '/n'.join(res.examples)
        self.single_word_info.visible = True
  
    def add_word_to_list_click(self, **event_args):
        """This method is called when the button is clicked"""
        res = anvil.server.call('add_word_to_list', self.word_input.text)
        if res.error:
            anvil.Notification(res.error, style="danger").show()
            return
        
        anvil.Notification(f"Word <strong>{self.word_input.text}</strong> added successfully", style="success").show()
        self.word_input.text = ""
        self.single_word_info.visible = False
        self.refresh_data_bindings()
