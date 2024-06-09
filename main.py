import os, time, random, json, codecs
from openai import OpenAI

client = OpenAI(api_key="sk-proj-0E2m3CHZ3VFJNrWzveQiT3BlbkFJi5VMPBOf1SHlkgfSDD5T")

# DIR_PREFIX = "vuln-founds"
DIR_PREFIX = "vuln-founds-gpt-4-turbo"
DIR_SMART_CONTRACTS = "smart-contracts"
SEVERITIES = ['High', 'Medium', 'Low', 'Informational']

def answer(query):
    persona = "You are an expert in identifying and analyzing vulnerabilities in Solidity-based smart contracts."

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": persona},
                {"role": "user", "content": query},
            ],
            model="gpt-4-turbo",
            temperature=0,
        )
        return response
    except Exception as e:
        print(f"Error querying: {e}")
        return {}


def query_smart_contract(source_code: str, file_name: str):
    responses = []

    for severity in SEVERITIES:
        # Build query
        query = build_query(severity, source_code)
        
        # Query
        res = answer(query)
        res = json.loads(res.model_dump_json())

        res["smart_contract"] = file_name
        res["query"] = query
        res["severity"] = severity

        responses.append(res)

        # Sleep for 1 second
        time.sleep(1)

    return responses


def build_query(severity_type : str, source_code: str):
    PROMPT_PATH = "prompt.txt"
    prompt, query = "", ""

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt = f.read()
        query = prompt.replace("{{severity_type}}", severity_type).replace("{{source_code}}", source_code)

    return query


def write_to_file(dir_prefix, responses):
    # Create a directory for the current timestamp
    timestamp = time.time().__str__().split(".")[0]
    directory = f"outputs/{dir_prefix}/{timestamp}"
    os.makedirs(f"{directory}", exist_ok=True)

    for res in responses:
        smart_contract = res["smart_contract"]
        severity = res["severity"]

        # Make directory for each severity
        severity_directory = f"{directory}/{severity}"
        os.makedirs(f"{severity_directory}", exist_ok=True)

        # Build file path
        file_path = f"{severity_directory}/{smart_contract}"

        try:
            # Write json
            with codecs.open(f"{file_path}.json", "w", encoding="utf-8") as f:
                json.dump(res, f, ensure_ascii=False, indent=2)

            # Write md
            with open(f"{file_path}.md", "w", encoding="utf-8") as f:
                f.write(res["choices"][0]["message"]["content"])

        except Exception as e:
            print(f"Error writing {smart_contract} to file: {e}")


if __name__ == "__main__":
    smart_contracts = []
    smart_contracts = os.listdir(DIR_SMART_CONTRACTS)

    for smart_contract in smart_contracts:
        if(smart_contract != 'relayer.sol') :
            with open(f"{DIR_SMART_CONTRACTS}/{smart_contract}", "r", encoding="UTF-8") as f:
                # Read smart contract source code
                source_code = f.read()
                
                print(f"Processing {smart_contract} ...")

                # Query on smart contract
                file_name = smart_contract.split(".")[0]
                responses = query_smart_contract(source_code, file_name)

                # Write query result to file
                write_to_file(DIR_PREFIX, responses)
