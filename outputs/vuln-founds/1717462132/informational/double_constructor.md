### 1. **Vulnerability Type**

**Severity:**
Informational

**Description:**
The constructor function is defined twice in the smart contract, which can lead to confusion and potential issues during contract deployment and initialization.

**Locations:**

- In the parent function:
  ```solidity
  constructor() public {
    admin = msg.sender;
  }
  ```

**Mitigation:**
Remove the redundant constructor function to avoid confusion and ensure clarity in contract initialization.