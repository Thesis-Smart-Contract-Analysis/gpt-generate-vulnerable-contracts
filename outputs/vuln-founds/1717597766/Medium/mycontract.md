### 1. **Using tx.origin for Authentication**

**Severity:**
Medium

**Description:**
Using `tx.origin` for authentication can lead to potential security vulnerabilities as it relies on the origin of the transaction, which can be manipulated in certain scenarios.

**Locations:**

- In the function `sendTo`:
  ```solidity
  require(tx.origin == owner);
  ```

**Mitigation:**
Avoid using `tx.origin` for authentication purposes as it can be spoofed. Instead, use `msg.sender` for verifying the sender's identity. Implement access control mechanisms based on `msg.sender` to ensure secure authentication.