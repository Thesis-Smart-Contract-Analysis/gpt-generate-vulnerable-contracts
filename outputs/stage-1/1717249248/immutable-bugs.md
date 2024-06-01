Here is a smart contract with Immutable Bugs vulnerability:

```solidity
// Smart contract with Immutable Bugs vulnerability
pragma solidity ^0.8.0;

contract ImmutableBug {
    uint private immutable secretNumber;

    constructor(uint _secretNumber) {
        secretNumber = _secretNumber;
    }

    function getSecretNumber() public view returns (uint) {
        return secretNumber;
    }

    function updateSecretNumber(uint _newSecretNumber) public {
        // This function should not be able to update the secretNumber, but due to Immutable Bugs vulnerability, it can.
        secretNumber = _newSecretNumber;
    }
}
```

In the above smart contract, the `secretNumber` variable is declared as `immutable` and initialized in the constructor. The intention is for the `secretNumber` to be set only once and not be changed thereafter. However, due to the Immutable Bugs vulnerability, the `updateSecretNumber` function can still modify the `secretNumber` variable, which goes against the intended immutability.

### Remediation:
To fix the Immutable Bugs vulnerability in the smart contract, you can follow these steps:

1. Remove the `updateSecretNumber` function or modify it to not update the `secretNumber` variable.
2. Ensure that once a variable is declared as `immutable`, it should not be modified in any function of the smart contract.
3. Use proper access control mechanisms to restrict the modification of sensitive variables.
4. Use proper testing and auditing to identify and fix vulnerabilities in the smart contract code.

Here is the remediated version of the smart contract:

```solidity
// Smart contract with Immutable Bugs vulnerability fixed
pragma solidity ^0.8.0;

contract ImmutableBugFixed {
    uint private immutable secretNumber;

    constructor(uint _secretNumber) {
        secretNumber = _secretNumber;
    }

    function getSecretNumber() public view returns (uint) {
        return secretNumber;
    }
}
```

In the remediated version, the `updateSecretNumber` function has been removed, ensuring that the `secretNumber` remains immutable as intended.