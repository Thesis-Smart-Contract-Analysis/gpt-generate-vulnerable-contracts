You are an expert in identifying and analyzing vulnerabilities in Solidity-based smart contracts.

Please thoroughly examine the smart contract source code to identify all potential vulnerabilities with "{{severity_type}}" severity, and provide strategies for mitigating them.

I want the results to cover all the following attributes: vulnerability type, vulnerability severity, description, locations, and mitigation. Below is an example format:

### 1. **show vulnerability type here**

**Severity:**
show vulnerability severity here

**Description:**
show description here

**Locations:**

- In the parent function:
  ```solidity
  code matched // Line of this code in the smart contract
  ```

**Mitigation:**
show mitigation here (You don't need to provide detailed examples for fixes; simply explain how to address the issues clearly)

Please analyze thoroughly and provide the most comprehensive and accurate results with exactly severity.

Below is the source code of the smart contract:
{{source_code}}
