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

Description: The vulnerability in the smart contract `AuthorizationVulnerability` lies in the line where the `transferOwnership` function uses `tx.origin` to check if the transaction sender is the owner. Using `tx.origin` for authorization can lead to a security vulnerability as it relies on the initial sender of the transaction, which can be manipulated in certain scenarios.

# Remediations

- Instead of using `tx.origin`, it is recommended to use `msg.sender` for authorization checks. `msg.sender` represents the direct caller of the function and is a more secure way to verify the sender's identity.
- Implement access control mechanisms such as modifiers or access control lists to manage authorization in a more secure and controlled manner.