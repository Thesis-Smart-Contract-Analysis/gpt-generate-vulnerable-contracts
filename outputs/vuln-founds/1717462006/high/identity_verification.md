### 1. **Vulnerability Type**

**Severity:**
High

**Description:**
The `isContract` function uses the `extcodesize` assembly operation to check if the given address is a contract. This method is not reliable for detecting contract addresses and can be manipulated by attackers to bypass intended functionality.

**Locations:**

- In the `isContract` function:
  ```solidity
  assembly { size := extcodesize(addr) }
  ```

**Mitigation:**
To improve the contract's security, consider using a more robust method to check if an address is a contract. One common approach is to use the `CODESIZE` opcode in EVM bytecode. Additionally, consider implementing additional checks or using libraries that provide more secure ways to determine if an address is a contract.