import os, time, random, json, codecs
from openai import OpenAI

client = OpenAI(api_key="sk-proj-0E2m3CHZ3VFJNrWzveQiT3BlbkFJi5VMPBOf1SHlkgfSDD5T")
ITERATIONS = 1
WITH_KB = False
DIR_PREFIX = "scenario-2-without-kb"

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
            model="gpt-3.5-turbo",
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

        print(f"Processing '{vuln_name}'...")
        already_queried.append(vuln_name)

        # Build query
        query = ""
        if kb is not None:
            query = build_query(vuln_name, kb)
        else:
            query = build_query_without_kb(vuln_name, vuln_description)
        if query == "":
            continue

        # Query
        res = answer(query)
        res = json.loads(res.model_dump_json())
        res["vuln_id"] = vuln_id
        if kb is None:
            res["query"] = query
        responses.append(res)

        # Sleep for 1 second
        time.sleep(1)

    return responses


def build_query(vuln_name, kb):
    PROMPT_PATH = "prompt.md"
    prompt, query = "", ""

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt = f.read()
        query = prompt.replace("{{vuln_name}}", vuln_name).replace("{{kb}}", kb)

    return query


def build_query_without_kb(vuln_name, vuln_description):
    PROMPT_PATH = "prompt_without_kb.md"
    prompt, query = "", ""

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt = f.read()
        query = prompt.replace("{{vuln_name}}", vuln_name).replace(
            "{{vuln_description}}", vuln_description
        )

    return query


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
        # Build file path
        vuln_id = res["vuln_id"]
        file_path = f"{directory}/{vuln_id}"

        try:
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
    for i in range(0, ITERATIONS):
        print(f"ITERATION {i+1}/{ITERATIONS}")
        responses = query_vulns(VULNS, kb)
        write_to_file(DIR_PREFIX, responses, kb)
