from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from main import load_vulns, build_kb, build_query

VULN_LIMIT = 10

client = OpenAI(api_key="sk-proj-qlgDp6WBcaaGXYrc1IJeT3BlbkFJUosuNsTcSO0Z13w2PQzN")


# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == "code_interpreter":
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)


if __name__ == "__main__":
    assistant = client.beta.assistants.create(
        name="Smart Contract Specialist",
        instructions="You are a senior smart contract developer and understand security vulnerabilities well.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-3.5-turbo",
    )

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=build_query("Re-entrancy", build_kb(load_vulns(), VULN_LIMIT)),
    )

    # Then, we use the `stream` SDK helper
    # with the `EventHandler` class to create the Run
    # and stream the response.
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()
