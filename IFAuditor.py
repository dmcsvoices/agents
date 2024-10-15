import openai
import os
import json
import sys

# Ensure that the API key is set
os.environ['OPENAI_API_KEY']
os.environ.get('OPENAI_API_KEY')

# Ensure that the user provides an output filename as an argument
if len(sys.argv) != 2:
   print("Usage: python script_name.py <output_file>")
   sys.exit(1)


output_file = sys.argv[1]

# Assistant information
Assistant_Name = "Infrastructure Auditor"
Assistant_FileName = "assistant_IFAuditor.json"
Assistant_Instructions = "You are a qualified Security Auditor and experienced AWS Cloud Architect. Your role is to review infrastructure implementation instructions.  When you receive an infrastructure description from the user, your task is to review the instructions from beginning to end, then provide a summary of the infrastructure that would created by the instructions.  Please format your output in an appropriate json format.  In your summary, call out any errors in the instructions, and provide limitations of the infrastructure that the user might need to know about. If you find the code you are given is incomplete, please try to analyze as much as you can understand, and if you do run into something that prevents you , output a sample of the input code that caused your error."
Assistant_Model = "gpt-4o-mini"
Assistant_ResponseFormat = "auto"

from openai import OpenAI

client = OpenAI()
#print(client.models.list())
# Load assistant file if there is one
if os.path.exists(Assistant_FileName):
    with open(Assistant_FileName, "r") as file:
        assistant = json.load(file)
        assistant = client.beta.assistants.retrieve(assistant['id'])
        print("Loaded assistant from file:")
else:
    assistant = client.beta.assistants.create(
        name=Assistant_Name,
        instructions=Assistant_Instructions,
        model=Assistant_Model,
        response_format=Assistant_ResponseFormat,
    )
    with open(Assistant_FileName, "w") as file:
        assistant_json = assistant.to_dict()
        json.dump(assistant_json, file)

#create the thread
thread = client.beta.threads.create()

# Take user input for infrastructure description
user_input = input("Describe the task:  ")


#print(user_input)

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_input
)


print("Your question has been accepted")

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)

print("Thinking......")

# Write the response to the specified output file
if run.status == 'completed':
    #print(run.response_format)
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print("Done thinking: ")
    with open(output_file, "w") as file:
        for message in messages.data:
            if message.content:
                for content_block in message.content:
                    #print(content_block.type)
                    if content_block.type == 'text':
                        text_value = content_block.text.value
                        # Write the content to the file
                        file.write(text_value + "\n")

    print(f"Output written to {output_file}")

else:
    print(run.status)

