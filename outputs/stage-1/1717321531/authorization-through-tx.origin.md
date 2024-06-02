# Smart contract

```solidity
pragma solidity ^0.4.24;

contract AuthorizationVulnerability {
    
    address public owner;

    function transferOwnership(address _newOwner) public {
        require(tx.origin == owner); // Vulnerable line
        owner = _newOwner;
    }
}
```

Description of the vulnerability in the above smart contract:
The vulnerability lies in the line `require(tx.origin == owner);` where the authorization check is based on `tx.origin`. Using `tx.origin` for authorization can be risky as it relies on the originating address of the transaction, which can be manipulated in certain scenarios.

# Remediations

- Use `msg.sender` instead of `tx.origin` for authorization checks. `msg.sender` represents the direct caller of the function and is a more secure way to verify the sender's identity.
- Implement a role-based access control system to manage ownership and permissions within the smart contract. This can provide a more robust and secure way to handle authorization.