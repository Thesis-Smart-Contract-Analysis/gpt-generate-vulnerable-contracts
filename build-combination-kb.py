from main import load_vulns


def build_combination_kb(vulns: list):
    kb = ""
    for vuln in vulns:
        vuln_id = vuln["id"]
        file_path = f"kb/{vuln_id}.md"
        with open(file_path, "r", encoding="utf-8") as f:
            kb += f.read()
    return kb


vulns = load_vulns()
kb = build_combination_kb()
with open("kb/combination-kb.md", "w", encoding="utf-8") as f:
    f.write(kb)
