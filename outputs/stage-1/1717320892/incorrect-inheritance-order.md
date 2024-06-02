# Smart contract with Incorrect Inheritance Order vulnerability

```solidity
pragma solidity ^0.8.0;

contract IncorrectInheritanceOrder {
    uint256 public data;

    constructor(uint256 _data) {
        data = _data;
    }
}

contract MaliciousContract is IncorrectInheritanceOrder {
    address public owner;

    constructor(uint256 _data) IncorrectInheritanceOrder(_data) {
        owner = msg.sender;
    }
}
```

Description: The vulnerability lies in the fact that the `MaliciousContract` inherits from `IncorrectInheritanceOrder` in the incorrect order. This can lead to unexpected behavior as the constructor of `MaliciousContract` will be executed before the constructor of `IncorrectInheritanceOrder`, potentially causing issues with the initialization of state variables.

# Remediations

- Ensure that the correct order of inheritance is maintained in the contract definitions.
- Always verify the order of inheritance to prevent unexpected behavior and ensure proper initialization of state variables.