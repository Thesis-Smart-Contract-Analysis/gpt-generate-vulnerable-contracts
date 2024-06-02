# Smart contract with Call to the Unknown vulnerability

```solidity
pragma solidity ^0.8.0;

contract VulnerableContract {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address _newOwner) public {
        owner.call(abi.encodeWithSignature("transferOwnership(address)", _newOwner)); // Vulnerability here
    }
}
```

Description: In the `transferOwnership` function of the smart contract, the `call` function is used to call a function on the `owner` address without verifying if the function exists. This can lead to unexpected behavior and potential security vulnerabilities.

# Remediations

- Use a known interface or function signature when using the `call` function to prevent calling unknown functions.
- Implement proper access control mechanisms to ensure only authorized users can call sensitive functions.