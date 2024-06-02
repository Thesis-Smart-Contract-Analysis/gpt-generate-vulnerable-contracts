# Smart contract with Call to the Unknown Vulnerability

```solidity
pragma solidity ^0.8.0;

contract CallToUnknownVulnerability {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address _newOwner) public {
        owner = _newOwner;
    }

    function unknownFunction(address _target) public {
        (bool success, ) = _target.call(abi.encodeWithSignature("unknownFunction()"));
        require(success);
    }
}
```

In the `unknownFunction` function, the vulnerability lies in the line where `_target.call` is used to call a function named `unknownFunction` on the address `_target`. If the function `unknownFunction` does not exist in the contract at the address `_target`, the call will still be successful, leading to unexpected behavior.

# Remediations

- Use a whitelist approach to ensure that the target address is a trusted contract with known functions.
- Implement a mechanism to verify the function signature before making the call to prevent calling unknown functions.