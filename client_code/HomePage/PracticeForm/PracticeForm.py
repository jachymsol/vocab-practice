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
        if "error" in res:
            anvil.Notification(res.get("error"), style="danger").show()
            return
        if not res.get("exists"):
            if anvil.confirm(f"The word {res.get('word')} does not exist. Do you want to remove it from the list?"):
                anvil.server.call("delete_word", res.get("word"))
                anvil.Notification(f"The word <strong>{res.get('word')}</strong> removed from the list.", style="success").show()
                return

        self.item["practice_word"] = res.get("word")
        self.item["practice_examples"] = "\n".join(res.get("examples"))
        self.item["practice_translation"] = res.get("translation")

        self.item["practice_translation_visible"] = False
        self.mark_practice_as_learned_button.enabled = True
        self.refresh_data_bindings()

    def start_practice_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        if anvil.users.get_user() == None:
            anvil.Notification("You must be logged in to start practicing", style="warning").show()
            return

        self.show_next_practice()

    def show_practice_translation_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.item["practice_translation_visible"] = True
        self.refresh_data_bindings()

    def mark_practice_as_learned_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        res = anvil.server.call("set_word_learned", self.item["practice_word"], True)
        if "error" in res:
            anvil.Notification(res.get("error"), style="danger").show()
            return

        self.mark_practice_as_learned_button.enabled = False
        anvil.Notification(f"Word <strong>{self.item['practice_word']}</strong> marked as learned successfully", style="success").show()

    def next_practice_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.show_next_practice()

    def view_translation_click(self, **event_args):
        """This method is called when the button is clicked"""
        res = anvil.server.call("get_translation", self.word_input.text)
        if "error" in res:
            anvil.Notification(res.get("error"), style="danger").show()
            return

        if res.get("exists"):
            self.single_word_info.content = res.get("translation") 
            self.single_word_info.visible = True
        else:
            self.single_word_info.content = f"The word _{self.word_input.text}_ does not exist."
            self.single_word_info.visible = True


    def view_word_examples_click(self, **event_args):
        """This method is called when the button is clicked"""
        res = anvil.server.call("get_examples", self.word_input.text)
        if "error" in res:
            anvil.Notification(res.get("error"), style="danger").show()
            return
        
        if res.get("exists"):
            self.single_word_info.content = '\n'.join(res.get("examples"))
            self.single_word_info.visible = True
        else:
            self.single_word_info.content = f"The word _{self.word_input.text}_ does not exist."
            self.single_word_info.visible = True

  
    def add_word_to_list_click(self, **event_args):
        """This method is called when the button is clicked"""
        if anvil.users.get_user() == None:
            anvil.Notification("You must be logged in to add a word", style="warning").show()
            return

        res = anvil.server.call("add_word_to_list", self.word_input.text)
        if "error" in res:
            anvil.Notification(res.get("error"), style="danger").show()
            return
        
        anvil.Notification(f"Word <strong>{self.word_input.text}</strong> added successfully", style="success").show()
        self.word_input.text = ""
        self.single_word_info.visible = False
        self.refresh_data_bindings()
