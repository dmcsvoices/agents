import openai
import os
import json
import sys

# Ensure that the API key is set
os.environ['OPENAI_API_KEY']
os.environ.get('OPENAI_API_KEY')

# Assistant information
Assistant_Name = "Infrastructure Expert"
Assistant_FileName = "assistant_IFExpert.json"
Assistant_Instructions = (
    "You are an AWS Solutions Architect. You understand all the AWS services and know which services to deploy and how "
    "best to implement apps in AWS. When asked to design a solution using AWS, you will return a high level overview of "
    "the system. A detailed description of the AWS services used and how they interact. After you describe the implementation, "
    "you will then provide a summary of the steps needed to take in the correct sequence, to implement the system. After this "
    "quick start summary, you will then generate a list of detailed instructions describing how to setup each required service, "
    "and give detailed instructions on any important specific settings or properties that need to be setup. Do not assume you can "
    "name a feature and expect the user to know exactly where the setting is. Format your output in JSON such that each summary "
    "level item is at the beginning of a JSON sub-heading, and any implementation instructions are formatted in JSON."
)
Assistant_Model = "gpt-4o"
Assistant_ResponseFormat = "json"

from openai import OpenAI

client = OpenAI()

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

thread = client.beta.threads.create()

# Take user input for infrastructure description
user_input = input("Describe the Infrastructure:  ")

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
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print("Done thinking: ")

    # Ensure that the user provides an output filename as an argument
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <output_file>")
        sys.exit(1)

    output_file = sys.argv[1]

    with open(output_file, "w") as file:
        for message in messages.data:
            if message.content:
                for content_block in message.content:
                    if content_block.type == 'text':
                        text_value = content_block.text.value
                        # Write the content to the file
                        file.write(text_value + "\n")

    print(f"Output written to {output_file}")

else:
    print(run.status)

