import json, random, time, os
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from main import load_vulns

DIR_PREFIX = "scenario-2-with-assistant"

client = OpenAI(api_key="sk-proj-qlgDp6WBcaaGXYrc1IJeT3BlbkFJUosuNsTcSO0Z13w2PQzN")


def build_kb(vulns: list, limit: int):
    kb = ""
    count = 0
    for vuln in vulns:
        if count == limit:
            break
        count += 1

        vuln_id = vuln["id"]
        file_path = f"kb/{vuln_id}.md"
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            kb += content

    return kb


def build_instructions(vulns: list):
    PROMPT_PATH = "assistant_instructions.md"
    prompt, instructions = "", ""

    kb = build_kb(vulns, len(vulns))
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt = f.read()
        instructions = prompt.replace("{{kb}}", kb)

    return instructions


def add_message(thread, vulns, id):
    vuln_name = ""
    for i in range(0, len(vulns)):
        vuln = vulns[i]
        if vuln["id"] == id:
            vuln_name = vulns[i]["name"]
    if vuln_name == "":
        return

    print(f"Add {vuln_name}")
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"\nPlease generate the source code of a smart contract with the {vuln_name} vulnerability and suggest remediations.",
    )


def build_thread(instructions, vulns, vuln_id):
    assistant = client.beta.assistants.create(
        name="Smart Contract Specialist",
        instructions=instructions,
        tools=[{"type": "code_interpreter"}],
        model="gpt-3.5-turbo",
    )
    thread = client.beta.threads.create()
    add_message(thread, vulns, vuln_id)
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
    vulns = load_vulns()
    instructions = build_instructions(vulns)
    vuln_id = "access-control-management"
    assistant, thread = build_thread(instructions, vulns, vuln_id)
    responses = run_thread(assistant, thread)
    print_messages(responses)
