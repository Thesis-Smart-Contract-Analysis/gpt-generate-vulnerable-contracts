### 1. **Avoid using tx.origin**

**Severity:**
High

**Description:**
Using `tx.origin` can lead to vulnerabilities as it represents the original sender of the transaction, which can be manipulated in certain scenarios.

**Locations:**

- In the function `sendTo`:
  ```solidity
  require(tx.origin == owner);
  ```

**Mitigation:**
Avoid using `tx.origin` for authorization checks as it can be spoofed. Instead, use `msg.sender` for authentication and authorization purposes.