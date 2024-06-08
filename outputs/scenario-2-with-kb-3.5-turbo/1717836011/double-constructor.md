# Smart contract

```solidity
pragma solidity ^0.4.22;

contract DoubleConstructorVulnerable {
    address public admin;

    function DoubleConstructorVulnerable() public {
        admin = address(0x0);
    }

    constructor() public {
        admin = msg.sender;
    }
}
```

Description of the vulnerability: The smart contract `DoubleConstructorVulnerable` contains both a function with the same name as the contract and a `constructor` function. This can lead to unexpected behavior as the order of execution of these functions is not guaranteed.

# Remediations

- Use only one constructor function in the smart contract to avoid ambiguity and ensure predictable behavior.
- Upgrade to Solidity versions after 0.4.22 where the double constructor issue is resolved.