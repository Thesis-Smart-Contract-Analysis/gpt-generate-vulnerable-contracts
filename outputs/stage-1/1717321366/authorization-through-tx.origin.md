# Smart contract

```solidity
pragma solidity ^0.4.24;

contract AuthorizationVulnerability {
    
    address public owner;

    function transferOwnership(address _newOwner) public {
        require(tx.origin == owner); // Vulnerability in this line
        owner = _newOwner;
    }
}
```

Description of the vulnerability: The vulnerability in the smart contract `AuthorizationVulnerability` lies in the line `require(tx.origin == owner)`. Using `tx.origin` for authorization can lead to a security vulnerability as it relies on the origin of the transaction, which can be manipulated by an attacker.

# Remediations

- **Remediation 1:** Instead of using `tx.origin`, it is recommended to use `msg.sender` for authorization checks. `msg.sender` represents the immediate sender of the transaction and is a more secure way to verify the caller's identity.

- **Remediation 2:** Implement access control mechanisms such as modifiers or access control lists to restrict access to sensitive functions based on the caller's address. This ensures that only authorized users can execute certain functions in the smart contract.