### 1. **Use of tx.origin for Authorization**

**Severity:**
Low

**Description:**
The use of `tx.origin` for authorization checks can lead to vulnerabilities where an attacker can trick a user into initiating a transaction that calls into a malicious contract, which then calls the vulnerable contract and passes the `tx.origin` check, as `tx.origin` will still be the original user. This is less severe in contexts where the risk of such phishing attacks is lower, but it's generally considered poor practice.

**Locations:**

- In the `sendTo` function:
  ```solidity
  require(tx.origin == owner); // Line 14
  ```

**Mitigation:**
Replace `tx.origin` with `msg.sender` for direct control checks. This ensures that the function can only be called directly by the owner, not by any contract on behalf of the owner. This change guards against the specific attack vector where `tx.origin` is manipulated by a malicious contract. Here's how you can modify the code:
```solidity
require(msg.sender == owner);
```
This change ensures that only the direct sender (who must be the owner) can call the function, enhancing security by preventing unauthorized access through contract calls.