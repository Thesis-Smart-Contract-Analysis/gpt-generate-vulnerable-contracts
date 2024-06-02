import json
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from main import load_vulns, build_kb, build_query, build_query_without_kb

client = OpenAI(api_key="sk-proj-qlgDp6WBcaaGXYrc1IJeT3BlbkFJUosuNsTcSO0Z13w2PQzN")

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
        content=build_query_without_kb(
            "Function Selector Clashing",
            "EVM sẽ dựa vào 4 byte đầu tiên trong dữ liệu của một giao dịch gọi hàm để thực thi hàm tương ứng. Tuy nhiên, 4 byte này dễ bị đụng độ giá trị băm và có thể dẫn đến việc smart contract thực thi một hàm nào đó mà người dùng không mong muốn.\nĐiều kiện của lỗ hổng là phải có sự tồn tại của proxy contract bởi vì trình biên dịch sẽ phát hiện ra hai hàm trong cùng một smart contract có 4 byte đầu trong giá trị băm trùng nhau.",
        ),
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        messages = messages.data[::-1]
        for message in messages:
            try:
                json_res = json.loads(message.model_dump_json())
                print(json.dumps(json_res, indent=2, ensure_ascii=False))
                print(json_res["content"][0]["text"]["value"])
            except json.JSONDecodeError:
                print("Invalid JSON in message")
    else:
        print(run.status)
