import os
import json

# Define vulnerability IDs
VULNERABILITY_IDS = [
    "function-or-state-variable-default-visibility",
    "integer-overflow-underflow",
    "outdated-compiler-version",
    "floating-compiler-version",
    "unchecked-return-value",
    "access-control-management",
    "re-entrancy",
    "uninitialized-storage-pointer",
    "assert-and-require-violation",
    "use-of-deprecated-solidity-functions",
    "delegatecall-to-untrusted-callee",
    "denial-of-service-with-failed-call",
    "authorization-through-tx.origin",
    "signature-malleability",
    "incorrect-constructor-name",
    "shadowing-state-variables",
    "weak-sources-of-randomness-from-chain-attributes",
    "missing-protection-against-signature-replay-attacks",
    "lack-of-proper-signature-verification",
    "write-to-arbitrary-storage-location",
    "incorrect-inheritance-order",
    "insufficient-gas-griefing",
    "arbitrary-jump-with-function-type-variable",
    "denial-of-service-with-block-gas-limit",
    "typographical-error",
    "right-to-left-override-control-unicode",
    "unexpected-balance",
    "hash-collisions-with-multiple-variable-length-arguments",
    "frozen-ether",
    "call-to-the-unknown",
    "hiding-malicious-code-with-external-contract",
    "double-constructor",
    "built-in-symbol-shadowing",
    "identity-verification",
    "immutable-bugs",
    "ether-lost-in-transfer",
    "stack-size-limit",
    "function-selector-clashing",
    "message-call-with-hardcoded-gas-amount",
    "short-address",
    "transaction-ordering-dependency",
    "timestamp-dependency",
    "unencrypted-private-data-on-chain",
    "untrustworthy-data-feeds",
]

def replace_in_file(file_path):
    # Function to replace characters in a file
    with open(file_path, "r", encoding="UTF-8") as file:
        content = file.read()

    content = content.replace("====", "##")
    content = content.replace("===", "#")

    with open(file_path, "w", encoding="UTF-8") as file:
        file.write(content)

def read_vulnerability(file_path):
    # Function to read vulnerability data from a file
    with open(file_path, "r", encoding="UTF-8") as file:
        content = file.read()
    lines = content.split("\n")
    identifier = file_path.split("\\")[-1].replace(".md", "")
    name = lines[0].replace("# ", "")
    return {"id": identifier, "name": name}

def sort_vulnerabilities(vulnerabilities):
    # Function to sort vulnerabilities based on predefined IDs
    sorted_vulnerabilities = []
    for identifier in VULNERABILITY_IDS:
        for vulnerability in vulnerabilities:
            if vulnerability["id"] == identifier:
                sorted_vulnerabilities.append(vulnerability)
    return sorted_vulnerabilities

def process_markdown_files(folder_path):
    # Function to process markdown files in a folder
    vulnerabilities = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                # replace_in_file(file_path) # Commented out for now
                vulnerabilities.append(read_vulnerability(file_path))
    sorted_vulnerabilities = sort_vulnerabilities(vulnerabilities)
    print(json.dumps(sorted_vulnerabilities, indent=4))

# Specify the folder path containing markdown files
folder_path = "kb"  # Update this with your folder path
process_markdown_files(folder_path)
