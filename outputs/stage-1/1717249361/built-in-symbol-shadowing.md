Below is a vulnerable smart contract with Built-in Symbol Shadowing vulnerability:

```solidity
pragma solidity ^0.8.0;

contract SymbolShadowing {
    uint256 public value;

    constructor(uint256 value) {
        value = value; // This assignment shadows the state variable 'value'
    }

    function updateValue(uint256 newValue) public {
        value = newValue; // This assignment updates the local variable 'value' instead of the state variable
    }
}
```

In the `SymbolShadowing` contract, the constructor parameter `value` shadows the state variable `value`, leading to confusion and unintended behavior. When the constructor is called, the assignment `value = value;` actually assigns the parameter value to itself instead of updating the state variable.

### Remediation:
To fix the Built-in Symbol Shadowing vulnerability, you should use a naming convention that distinguishes between state variables and local variables. Here's the remediated version of the contract:

```solidity
pragma solidity ^0.8.0;

contract SymbolShadowingFixed {
    uint256 public storedValue;

    constructor(uint256 _value) {
        storedValue = _value; // Use a different name for the parameter to avoid shadowing
    }

    function updateValue(uint256 newValue) public {
        storedValue = newValue; // Update the state variable 'storedValue'
    }
}
```

In the remediated `SymbolShadowingFixed` contract, the state variable `storedValue` is used instead of `value` to avoid shadowing. By using distinct names for state variables and local variables, the vulnerability is mitigated.