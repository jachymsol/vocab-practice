import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def get_translation(word):
  return "Table"

@anvil.server.callable
def get_examples(word):
  return """1. Der Tisch im Esszimmer ist aus massivem Holz.
2. Kannst du bitte den Tisch decken?
3. Wir haben einen neuen Tisch für das Büro gekauft."""

@anvil.server.callable
def get_pracice_examples():
  return get_examples("Tisch")