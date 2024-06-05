### 1. **SWE-115: Use of tx.origin**

**Severity:**
Informational

**Description:**
The use of `tx.origin` can introduce security vulnerabilities as it represents the original sender of the transaction, which can be a contract calling the function. Relying on `tx.origin` for authentication or authorization checks can lead to potential exploits.

**Locations:**

- In the function `sendTo`:
  ```solidity
  require(tx.origin == owner);
  ```

**Mitigation:**
Avoid using `tx.origin` for authentication or authorization checks. Instead, use `msg.sender` to verify the immediate caller of the function. Consider implementing access control mechanisms such as modifiers to restrict access to certain functions based on the caller's address.