import anvil.email
import os
import json
import jsonschema
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


def get_response_batch(content, assistant):
  thread = client.beta.threads.create()
  client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=str(content)
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


def verify_response(response, schema):
  try:
    jsonschema.validate(response, schema)
    return True
  except jsonschema.ValidationError:
    return False


def get_examples(language, word, num_examples):
  model_input = {"language": language, "word": word, "num_examples": num_examples}
  output_schema = {
    "type": "object",
    "properties": {
      "exists": {"type": "boolean"},
      "examples": {"type": "array", "items": {"type": "string"}},
    },
    "additionalProperties": False,
  }

  num_attempts_left = 3
  while True:
    try:
      model_output = get_response_batch(model_input, examples_assistant)
      response = json.loads(model_output)
      verify_response(response, output_schema)
      return response
    except (json.JSONDecodeError, jsonschema.ValidationError) as e:
      if num_attempts_left == 0:
        raise Exception(f"Error getting examples: {e}")
      num_attempts_left -= 1
      continue


def get_translation(language, word):
  model_input = {"language": language, "word": word}
  output_schema = {
    "type": "object",
    "properties": {
      "exists": {"type": "string"},
      "translation": {"type": "string"}
    },
    "additionalProperties": False,
  }

  num_attempts_left = 3
  while True:
    try:
      model_output = get_response_batch(model_input, translations_assistant)
      response = json.loads(model_output)
      verify_response(response, output_schema)
      return response
    except (json.JSONDecodeError, jsonschema.ValidationError) as e:
      if num_attempts_left == 0:
        raise Exception(f"Error getting translation: {e}")
      num_attempts_left -= 1
      continue
