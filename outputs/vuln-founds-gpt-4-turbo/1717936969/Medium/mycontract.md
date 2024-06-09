### 1. **Use of tx.origin for Authorization**

**Severity:**
Medium

**Description:**
The use of `tx.origin` for authorization checks can lead to security vulnerabilities known as "phishing attacks." The `tx.origin` variable returns the original external account that started the transaction chain, which means it will always point to the externally owned account (EOA) that initiated the transaction. If a contract calls another contract, which then calls this contract, `tx.origin` will still refer to the initial external caller, not the immediate caller (`msg.sender`). Malicious contracts can exploit this by tricking users into interacting with them, which then call the vulnerable contract, passing the `tx.origin` check if the user is the owner.

**Locations:**

- In the `sendTo` function:
  ```solidity
  require(tx.origin == owner); // Line 12
  ```

**Mitigation:**
Replace `tx.origin` with `msg.sender` for authorization checks. `msg.sender` refers to the immediate caller of the function, which is more secure for access control. This change ensures that only the direct caller, who must be the owner, can execute sensitive functions. Here's how you can modify the code:

```solidity
require(msg.sender == owner);
```

This modification will prevent attackers from exploiting the contract through a phishing attack, as they would need to control the direct calling account, not just any account in the transaction chain.