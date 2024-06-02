# Smart contract with Incorrect Inheritance Order vulnerability

```solidity
pragma solidity ^0.8.0;

contract IncorrectInheritanceOrder {
    // Incorrect Inheritance Order vulnerability on the following line
    contract A {
        uint public num;

        constructor(uint _num) {
            num = _num;
        }
    }

    contract B is A {
        uint public data;

        constructor(uint _num, uint _data) A(_num) {
            data = _data;
        }
    }
}
```

## Description

In the above smart contract, the vulnerability lies in the incorrect order of inheritance. Contract `B` is inheriting from contract `A`, but contract `A` is defined inside contract `B`. This can lead to unexpected behavior and potential security risks.

## Remediations

- Define contract `A` outside of contract `B` to ensure proper inheritance order.
- Ensure that the inheritance hierarchy is clearly defined and follows the correct order to avoid any ambiguity or vulnerabilities.