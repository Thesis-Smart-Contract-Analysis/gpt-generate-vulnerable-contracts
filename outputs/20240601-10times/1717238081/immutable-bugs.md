Below is a vulnerable smart contract with Immutable Bugs vulnerability:

```solidity
// Vulnerable smart contract with Immutable Bugs vulnerability
pragma solidity ^0.8.0;

contract ImmutableBug {
    uint private immutable secretNumber;

    constructor(uint _secretNumber) {
        secretNumber = _secretNumber;
    }

    function getSecretNumber() public view returns(uint) {
        return secretNumber;
    }

    function updateSecretNumber(uint _newSecretNumber) public {
        secretNumber = _newSecretNumber; // Vulnerable point
    }
}
```

In the above smart contract, the `secretNumber` variable is declared as `immutable`, meaning it cannot be changed after initialization. However, there is a vulnerability in the `updateSecretNumber` function where an attempt is made to update the `secretNumber`, which is not allowed due to the `immutable` keyword.

### Remediation:
To fix the Immutable Bugs vulnerability in the smart contract, you should remove the attempt to update the `immutable` variable. Here is the remediated version of the smart contract:

```solidity
// Fixed smart contract with Immutable Bugs vulnerability remediated
pragma solidity ^0.8.0;

contract ImmutableBugFixed {
    uint private immutable secretNumber;

    constructor(uint _secretNumber) {
        secretNumber = _secretNumber;
    }

    function getSecretNumber() public view returns(uint) {
        return secretNumber;
    }
}
```

In the remediated version, the `updateSecretNumber` function has been removed to prevent any attempt to update the `immutable` variable `secretNumber`. This ensures that the `secretNumber` remains immutable after initialization, eliminating the Immutable Bugs vulnerability.