import json, random, time, os
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from main import VULNS, VULN_LIMIT, build_kb, build_query, build_query_without_kb

DIR_PREFIX = "scenario-2-with-assistant"

client = OpenAI(api_key="sk-proj-0E2m3CHZ3VFJNrWzveQiT3BlbkFJi5VMPBOf1SHlkgfSDD5T")

def build_instructions():
    PROMPT_PATH = "assistant_instructions.md"
    prompt, instructions = "", ""

    kb = build_kb(VULNS, VULN_LIMIT)
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt = f.read()
        instructions = prompt.replace("{{kb}}", kb)

    return instructions

def add_message(thread, id):
    vuln_name = ""
    for i in range(0, len(VULNS)):
        vuln = VULNS[i]
        if vuln["id"] == id:
            vuln_name = VULNS[i]["name"]
    if vuln_name == "":
        return
    
    print(f"Add {vuln_name}")
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"\nPlease generate the source code of a smart contract with the {vuln_name} vulnerability and suggest remediations.",
    )

def build_thread(instructions, vuln_id):
    assistant = client.beta.assistants.create(
        name="Smart Contract Specialist",
        instructions=instructions,
        tools=[{"type": "code_interpreter"}],
        model="gpt-4",
    )
    thread = client.beta.threads.create()
    add_message(thread, vuln_id)
    return (assistant, thread)
    

def run_thread(assistant, thread):
    print("Running thread...")
    run = client.beta.threads.runs.create_and_poll(
        assistant_id=assistant.id,
        thread_id=thread.id,
    )

    responses = []
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        messages = messages.data[::-1]
        for i in range(0, len(messages)):
            message = messages[i]
            try:
                json_res = json.loads(message.model_dump_json())
                responses.append(json_res)
            except json.JSONDecodeError as e:
                print("Invalid JSON in message: {e}")
        return responses
    else:
        print(run.status)

def print_messages(messages):
    for message in messages:
        print(json.dumps(message, indent=4, ensure_ascii=False))
        print()
        print(message["content"][0]["text"]["value"])

if __name__ == "__main__":
    instructions = build_instructions()
    vuln_id = "access-control-management"
    assistant, thread = build_thread(instructions, vuln_id)
    responses = run_thread(assistant, thread)
    print_messages(responses)
    

    


