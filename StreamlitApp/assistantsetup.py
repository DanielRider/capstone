from openai import OpenAI
import os
import time
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')


class Assistant:
  def __init__(self, userfilepath):
      self.client = OpenAI(
        api_key='',
      )
      self.assistant_id = 'asst_nuA2fHeOmt0TIP6pfjNXDQi1'
      self.userfilepath = userfilepath
      self.run = None
      self.thread = None
      self.file = None
      self.latest_message = None
      self.message_list = None


  def getFile(self):
      self.file = self.client.files.create(
        file=open(self.userfilepath, "rb"),
        purpose='assistants'
      )

  def generateThread(self):
      self.thread = self.client.beta.threads.create(
        messages=[
          {
            "role": "user",
            "content": "I need help with preventing and managing diabeties. Here is my data. Limit response to one paragraph",
            "file_ids": [self.file.id]
          }
        ]
      )

  def generateRun(self):
      self.run = self.client.beta.threads.runs.create(
        thread_id=self.thread.id,
        assistant_id=self.assistant_id
      )

  def submit_message(self,user_message):
      self.client.beta.threads.messages.create(
          thread_id=self.thread.id, role="user", content=user_message
      )
      return self.client.beta.threads.runs.create(
          thread_id=self.thread.id,
          assistant_id=self.assistant_id,
      )

  def get_response(self):
      self.message_list = self.client.beta.threads.messages.list(thread_id=self.thread.id, order="asc")
      return

  def retrieveMessage(self):
    # Retrieve the message object
    self.get_response()
    last_message_id = self.message_list.last_id
    message = self.client.beta.threads.messages.retrieve(
      thread_id=self.thread.id,
      message_id=last_message_id
    )

    # Extract the message content
    message_content = message.content[0].text
    annotations = message_content.annotations
    citations = []

    # Iterate over the annotations and add footnotes
    for index, annotation in enumerate(annotations):
      # Replace the text with a footnote
      message_content.value = message_content.value.replace(annotation.text, f' [{index}]')

      # Gather citations based on annotation attributes
      if (file_citation := getattr(annotation, 'file_citation', None)):
        cited_file = self.client.files.retrieve(file_citation.file_id)
        citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
      elif (file_path := getattr(annotation, 'file_path', None)):
        cited_file = self.client.files.retrieve(file_path.file_id)
        citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
        # Note: File download functionality not implemented above for brevity

    # Add footnotes to the end of the message before displaying to user
    message_content.value += '\n' + '\n'.join(citations)
    return message_content

  def pretty_print(self):
      print("# Messages")
      for m in self.message_list:
          print(f"{m.role}: {m.content[0].text.value}")
      print()

  def wait_on_run(self):
      while self.run.status == "queued" or self.run.status == "in_progress":
          self.run = self.client.beta.threads.runs.retrieve(
              thread_id=self.thread.id,
              run_id=self.run.id,
          )
          # print(self.run.status)
          time.sleep(0.5)
      return self.run


# testassistant = Assistant("patient1.csv")csv
# run1 = testassistant.wait_on_run()
# print(testassistant.retrieveMessage())

# try:
#     print(testassistant.retrieveMessage())
# except Exception as e:
#     print(f'error {e}')
# finally:
#     testassistant.get_response()
#     testassistant.pretty_print()







