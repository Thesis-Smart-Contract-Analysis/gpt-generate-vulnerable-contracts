Below is a vulnerable smart contract with Incorrect Inheritance Order vulnerability:

```solidity
pragma solidity ^0.8.0;

contract Base {
    uint public baseValue;

    constructor(uint _value) {
        baseValue = _value;
    }
}

contract Child is Base {
    uint public childValue;

    constructor(uint _baseValue, uint _childValue) Base(_baseValue) {
        childValue = _childValue;
    }
}
```

In the above smart contract, the `Child` contract inherits from the `Base` contract. However, the order of inheritance is incorrect. The `Child` contract should first inherit from `Base` and then define its own variables and functions. This incorrect order can lead to unexpected behavior and potential security vulnerabilities.

### Remediation:
To fix the Incorrect Inheritance Order vulnerability, you should ensure that the child contract inherits from the base contract before defining its own variables and functions. Here is the remediated version of the smart contract:

```solidity
pragma solidity ^0.8.0;

contract Base {
    uint public baseValue;

    constructor(uint _value) {
        baseValue = _value;
    }
}

contract Child is Base {
    uint public childValue;

    constructor(uint _baseValue, uint _childValue) Base(_baseValue) {
        childValue = _childValue;
    }
}
```

By following the correct order of inheritance, you can prevent potential issues related to the Incorrect Inheritance Order vulnerability.