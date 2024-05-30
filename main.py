import os
import openai
import time
import random
import json

openai.api_key = "sk-proj-qlgDp6WBcaaGXYrc1IJeT3BlbkFJUosuNsTcSO0Z13w2PQzN"
VULN_LIMIT = 10


def load_vulns():
    with open(f"kb/vulns.json", "r", encoding="UTF-8") as f:
        vulns = f.read()
    return json.loads(vulns)


def build_kb(vulns: list, limit: int):
    kb = "Use the below information to do the task\n"
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


def answer(kb, query):
    try:
        response = openai.ChatCompletion.create(
            messages=[
                {
                    "role": "system",
                    "content": "You generate vulnerable smart contract and suggest remediation for the vulnerabilities.",
                },
                {"role": "user", "content": kb},
                {"role": "assistant", "content": "Okay sure!"},
                {"role": "user", "content": query},
            ],
            model="gpt-3.5-turbo",
            temperature=0,
        )
        return response
    except openai.error.RateLimitError as e:
        return {"error": e}


def query_vulns(vulns: list, kb: str):
    already_queried = []
    vuln_name = ""
    responses = []

    for i in range(1, VULN_LIMIT):
        # Get a random vulnerability
        while vuln_name in already_queried or vuln_name == "":
            random_index = random.randint(0, len(vulns) - 1)
            vuln_name = vulns[random_index]["name"]
            vuln_id = vulns[random_index]["id"]
        
        print(f"Processing '{vuln_name}'...")
        already_queried.append(vuln_name)

        # Build query
        query = f"Generate a smart contract that has {vuln_name} vulnerability and suggest remediation for the vulnerability."

        # Query
        res = answer(kb, query)
        res["query"] = query
        res["kb"] = kb
        res["vuln_id"] = vuln_id
        responses.append(res)

    return responses


def write_to_file(responses):
    for res in responses:
        # Create a directory for the current date
        timestr = time.strftime("%Y%m%d")
        os.makedirs(f"outputs/{timestr}", exist_ok=True)

        # Build file path
        vuln_id = res["vuln_id"]
        file_path = f"outputs/{timestr}/{vuln_id}"

        # Write json
        with open(f"{file_path}.json", "w") as f:
            f.write(res.__str__())

        # Write md
        with open(f"{file_path}.md", "w") as f:
            f.write(res["choices"][0]["message"]["content"])


vulns = load_vulns()
kb = build_kb(vulns, VULN_LIMIT)
responses = query_vulns(vulns, kb)
write_to_file(responses)
