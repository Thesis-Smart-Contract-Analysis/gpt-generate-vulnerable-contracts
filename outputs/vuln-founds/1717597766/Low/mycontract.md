### 1. **Solidity Weaknesses and Vulnerabilities (SWE-115)**

**Severity:**
Low

**Description:**
The use of `tx.origin` can introduce security vulnerabilities as it represents the original sender of a transaction, which can be manipulated in certain scenarios. Relying on `tx.origin` for authentication or authorization checks can lead to potential security risks.

**Locations:**

- In the function `sendTo`:
  ```solidity
  require(tx.origin == owner);
  ```

**Mitigation:**
Avoid using `tx.origin` for authentication or authorization checks. Instead, use `msg.sender` for verifying the immediate caller of the function. This helps in preventing potential attacks that exploit the `tx.origin` property.