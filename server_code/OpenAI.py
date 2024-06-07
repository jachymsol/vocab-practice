import os
from openai import AssistantEventHandler, OpenAI
from openai.types.beta.threads import Text
from typing_extensions import override
from dotenv import load_dotenv


EXAMPLE_ASSISTANT_ID = "asst_FxrmP4ZebEu5IaReBSSJSZzX"
TRANSLATION_ASSISTANT_ID = "asst_hij1AS8ekMYhBvYnvJMG2e3U"


class EventHandler(AssistantEventHandler):
  @override
  def on_text_created(self, text: Text) -> None:
    print(flush=True)

  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)


if not os.getenv('OPENAI_API_KEY'):
  load_dotenv('Vocabulary_Practice/.env')

client = OpenAI()
examples_assistant = client.beta.assistants.retrieve(EXAMPLE_ASSISTANT_ID)
translations_assistant = client.beta.assistants.retrieve(TRANSLATION_ASSISTANT_ID)


def get_response_stream(word, assistant):
  thread = client.beta.threads.create()
  client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=word
  )
  with client.beta.threads.runs.stream(
    assistant_id=assistant.id,
    thread_id=thread.id,
    event_handler=EventHandler()
  ) as stream:
    stream.until_done()
  return 


def get_response_batch(word, assistant):
  thread = client.beta.threads.create()
  client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=word
  )
  run = client.beta.threads.runs.create_and_poll(
    assistant_id=assistant.id,
    thread_id=thread.id
  )
  if run.status == 'completed':
    response = client.beta.threads.messages.list(thread_id=thread.id, limit=1)
    return response.data[0].content[0].text.value
  else:
    return run.status


def get_examples(word):
  return get_response_batch(word, examples_assistant)


def get_translation(word):
  return get_response_batch(word, translations_assistant)
