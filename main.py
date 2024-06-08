import os, time, random, json, codecs
from openai import OpenAI

client = OpenAI(api_key="sk-proj-0E2m3CHZ3VFJNrWzveQiT3BlbkFJi5VMPBOf1SHlkgfSDD5T")
ITERATIONS = 1
WITH_KB = True
SINGLE_VULN = True
VULN_ID = "assert-and-require-violation"
DIR_PREFIX = "scenario-2-with-kb"
MODEL = "gpt-4-turbo"


def load_vulns():
    with open(f"kb/vulns.json", "r", encoding="UTF-8") as f:
        vulns = f.read()
    return json.loads(vulns)


VULNS = load_vulns()
VULN_LIMIT = len(VULNS)


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


def answer(query):
    persona = "You are a senior smart contract developer and understand security vulnerabilities well."

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": persona},
                {"role": "user", "content": query},
            ],
            model=MODEL,
            temperature=0,
        )
        return response
    except Exception as e:
        print(f"Error querying: {e}")
        return {}


def query_vulns(vulns: list, kb: str):
    already_queried = []
    vuln_name = ""
    responses = []

    for i in range(0, VULN_LIMIT):
        # Get a random vulnerability
        while vuln_name in already_queried or vuln_name == "":
            random_index = random.randint(0, len(vulns) - 1)
            vuln_name = vulns[random_index]["name"]
            vuln_id = vulns[random_index]["id"]
            vuln_description = vulns[random_index]["description"]
        already_queried.append(vuln_name)

        print(f"Processing '{vuln_name}'...")

        # Build query
        query = build_query(vuln_name, vuln_description, kb)
        if query == "":
            continue

        # Query
        res = send_query(query, vuln_id)
        print(f"Response: {json.dumps(res, indent=2)}")
        responses.append(res)

        # Sleep for 1 second
        time.sleep(1)

    return responses


def query_vuln(vuln: dict, kb: dict) -> dict:
    vuln_name, vuln_description, vuln_id = vuln["name"], vuln["description"], vuln["id"]
    print(f"Processing '{vuln_name}'...")
    query = build_query(vuln_name, vuln_description, kb)
    res = send_query(query, vuln_id)
    print(f"Response: {json.dumps(res, indent=2)}")
    return res


def build_query(vuln_name: str, vuln_description: str, kb: dict) -> str:
    query = ""
    if kb is not None:
        query = build_query_with_kb(vuln_name, kb)
    else:
        query = build_query_without_kb(vuln_name, vuln_description)
    return query


def build_query_with_kb(vuln_name, kb) -> str:
    PROMPT_PATH = "prompt.md"
    prompt, query = "", ""

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt = f.read()
        query = prompt.replace("{{vuln_name}}", vuln_name).replace("{{kb}}", kb)

    return query


def build_query_without_kb(vuln_name, vuln_description) -> str:
    PROMPT_PATH = "prompt_without_kb.md"
    prompt, query = "", ""

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt = f.read()
        query = prompt.replace("{{vuln_name}}", vuln_name).replace(
            "{{vuln_description}}", vuln_description
        )

    return query


def send_query(query, vuln_id) -> dict:
    res = answer(query)
    res = json.loads(res.model_dump_json())
    res["vuln_id"] = vuln_id
    if kb is None:
        res["query"] = query
    return res


def write_to_file(dir_prefix, responses, kb):
    # Create a directory for the current timestamp
    timestamp = time.time().__str__().split(".")[0]
    directory = f"outputs/{dir_prefix}/{timestamp}"
    os.makedirs(f"{directory}", exist_ok=True)

    # Write kb if not exists
    if kb is not None:
        if not os.path.exists(f"outputs/{dir_prefix}/kb.md"):
            with open(f"outputs/{dir_prefix}/kb.md", "w", encoding="utf-8") as f:
                f.write(kb)

    for res in responses:
        try:
            # Build file path
            vuln_id = res["vuln_id"]
            file_path = f"{directory}/{vuln_id}"

            # Write json
            with codecs.open(f"{file_path}.json", "w", encoding="utf-8") as f:
                json.dump(res, f, ensure_ascii=False, indent=2)

            # Write md
            with open(f"{file_path}.md", "w", encoding="utf-8") as f:
                f.write(res["choices"][0]["message"]["content"])
        except Exception as e:
            print(f"Error writing {vuln_id} to file: {e}")


if __name__ == "__main__":
    kb = build_kb(VULNS, VULN_LIMIT) if WITH_KB else None
    if SINGLE_VULN:
        for vuln in VULNS:
            if vuln["id"] != VULN_ID:
                continue
            res = query_vuln(vuln, kb)
            write_to_file(DIR_PREFIX, [res], kb)
    else:
        for i in range(0, ITERATIONS):
            print(f"ITERATION {i+1}/{ITERATIONS}")
            responses = query_vulns(VULNS, kb)
            write_to_file(DIR_PREFIX, responses, kb)
