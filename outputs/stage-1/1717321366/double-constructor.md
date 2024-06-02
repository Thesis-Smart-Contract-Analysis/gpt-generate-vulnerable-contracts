# Smart contract

```solidity
pragma solidity ^0.4.24;

contract DoubleConstructorVulnerability {
    
    uint public data;

    constructor() public {
        data = 1;
    }

    constructor() public {
        data = 2;
    }
}
```

The vulnerability lies in having two constructor functions in the same smart contract, which is not allowed in Solidity. This can lead to unexpected behavior and potential security risks.

# Remediations

- **Remediation 1:** Remove one of the constructor functions and consolidate the initialization logic into a single constructor.
- **Remediation 2:** Use an initializer function pattern along with a flag to ensure that initialization logic is only executed once.

By addressing the Double Constructor vulnerability, you can enhance the security and integrity of your smart contract.