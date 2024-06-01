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
        secretNumber = _newSecretNumber; // This will cause an error due to attempting to modify an immutable variable
    }
}
```

In the smart contract `ImmutableBug` above, the variable `secretNumber` is declared as `immutable`, meaning it cannot be modified after initialization. However, the function `updateSecretNumber` tries to update the `secretNumber`, which will result in a compilation error due to attempting to modify an immutable variable.

### Remediation:
To fix the Immutable Bugs vulnerability, you should ensure that immutable variables are only assigned a value once during contract deployment and cannot be modified thereafter. If you need to update a value, consider using a regular state variable instead of an immutable one.

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

In the remediated version, the `updateSecretNumber` function has been removed, ensuring that the `secretNumber` remains immutable and cannot be modified after deployment.