# Smart contract

```solidity
pragma solidity ^0.4.24;

contract IncorrectInheritanceOrder {
    
    uint256 public data;

    function setData(uint256 _data) public {
        data = _data;
    }
}

contract MaliciousContract is IncorrectInheritanceOrder {
    
    address public owner;

    function setOwner(address _owner) public {
        owner = _owner;
    }
}
```

Description: The `MaliciousContract` inherits from `IncorrectInheritanceOrder` in the incorrect order, where the base contract should come after the derived contract. This can lead to unexpected behavior and security vulnerabilities.

# Remediations

- Ensure that the base contract is inherited before the derived contract in the inheritance list.
- Correct the inheritance order by placing `IncorrectInheritanceOrder` after `MaliciousContract` in the contract definition.