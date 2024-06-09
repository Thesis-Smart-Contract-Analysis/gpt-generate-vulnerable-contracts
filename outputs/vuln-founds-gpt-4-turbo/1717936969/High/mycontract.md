### 1. **Use of tx.origin for Authorization**

**Severity:**
High

**Description:**
The use of `tx.origin` for authorization checks is considered a security risk. `tx.origin` checks the original external account that started the transaction, not the immediate caller (which could be another contract). This can lead to vulnerabilities where an attacker tricks a user into interacting with a malicious contract that then calls into a legitimate contract, passing the `tx.origin` check if the user is the original transaction starter.

**Locations:**

- In the `sendTo` function:
  ```solidity
  require(tx.origin == owner); // Line 12
  ```

**Mitigation:**
Replace `tx.origin` with `msg.sender` for authorization checks. `msg.sender` refers to the immediate caller of the function, which is more secure in the context of contracts calling other contracts. This change ensures that only the contract or user directly interacting with the function can pass the authorization check, not any originating external account. Here's how you can modify the code:

Replace:
```solidity
require(tx.origin == owner);
```
With:
```solidity
require(msg.sender == owner);
```

This change will effectively mitigate the risk associated with the misuse of `tx.origin` and enhance the security of the contract by ensuring that only the intended and legitimate entities can execute sensitive functions.