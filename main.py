import os, time, random, json, codecs
from openai import OpenAI

client = OpenAI(api_key="sk-proj-0E2m3CHZ3VFJNrWzveQiT3BlbkFJi5VMPBOf1SHlkgfSDD5T")

WITH_KB = True
DIR_PREFIX = "scenario-2-with-kb"
MODEL = "gpt-4-turbo"

SINGLE_VULN = True
VULN_ID = "typographical-error"

WITH_COMBINATION_KB = True
COMBINATION_KB_PATH = "kb/combination-kb.md"
COMBINATION_KB = ""


def load_vulns() -> dict:
    with open(f"kb/vulns.json", "r", encoding="UTF-8") as f:
        vulns = f.read()
    return json.loads(vulns)


def load_kb(vulns: list):
    for vuln in vulns:
        vuln_id = vuln["id"]
        file_path = f"kb/{vuln_id}.md"
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            vuln["kb"] = content


def load_combination_kb():
    global COMBINATION_KB
    with open(COMBINATION_KB_PATH, "r", encoding="utf-8") as f:
        COMBINATION_KB = f.read()


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


def query_vulns(vulns: list) -> list:
    responses = []
    for vuln in vulns:
        id, name, description, kb = (
            vuln["id"],
            vuln["name"],
            vuln["description"],
            vuln["kb"] if "kb" in vuln else None,
        )

        # Build query
        print(f"Request '{name}'...")
        query = build_query(name, description, kb)
        if query == "":
            continue

        # Query
        res = send_query(query, id, kb)
        print(f"Response: {json.dumps(res, indent=2, ensure_ascii=False)}")
        responses.append(res)

        # Sleep for 1 second
        time.sleep(1)

    return responses


def query_vuln(vuln: dict) -> dict:
    id, name, description, kb = (
        vuln["id"],
        vuln["name"],
        vuln["description"],
        vuln["kb"] if "kb" in vuln else None,
    )

    if WITH_COMBINATION_KB:
        kb = COMBINATION_KB

    print(f"Request '{name}'...")
    query = build_query(name, description, kb)

    res = send_query(query, id, kb)
    print(f"Response: {json.dumps(res, indent=2, ensure_ascii=False)}")
    return res


def build_query(name: str, description: str, kb: str) -> str:
    query = ""
    if kb is not None:
        query = build_query_with_kb(name, kb)
    else:
        query = build_query_without_kb(name, description)
    return query


def build_query_with_kb(name, kb) -> str:
    PROMPT_PATH = "prompts/prompt.md"
    prompt, query = "", ""

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt = f.read()
        query = prompt.replace("{{vuln_name}}", name).replace("{{kb}}", kb)

    return query


def build_query_without_kb(name, description) -> str:
    PROMPT_PATH = "prompts/prompt_without_kb.md"
    prompt, query = "", ""

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt = f.read()
        query = prompt.replace("{{vuln_name}}", name).replace(
            "{{vuln_description}}", description
        )

    return query


def send_query(query: str, id: str, kb: str) -> dict:
    res = answer(query)
    res = json.loads(res.model_dump_json())
    res["vuln_id"] = id
    res["query"] = query
    return res


def write_to_file(dir_prefix: str, responses: list):
    # Create a directory for the current timestamp
    timestamp = time.time().__str__().split(".")[0]
    directory = f"outputs/{dir_prefix}/{timestamp}"
    os.makedirs(f"{directory}", exist_ok=True)

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
    vulns = load_vulns()
    if WITH_KB:
        load_kb(vulns)
    if WITH_COMBINATION_KB:
        load_combination_kb()

    if SINGLE_VULN:
        for vuln in vulns:
            if vuln["id"] != VULN_ID:
                continue
            res = query_vuln(vuln)
            write_to_file(DIR_PREFIX, [res])
    else:
        responses = query_vulns(vulns)
        write_to_file(DIR_PREFIX, responses)
