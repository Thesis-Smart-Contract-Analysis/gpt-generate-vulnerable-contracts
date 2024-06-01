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

    function getValue() public view returns (uint256) {
        return value; // This returns the local variable 'value' instead of the state variable
    }
}
```

In the `SymbolShadowing` contract above, the constructor and the `updateValue` function are using the same variable name `value` for the function parameter as well as the state variable. This leads to the state variable `value` being shadowed by the local variable `value`, causing unexpected behavior where the state variable is not updated as intended.

### Remediation:
To fix the Built-in Symbol Shadowing vulnerability, you should use a different variable name for the function parameter to avoid shadowing the state variable. Here is the remediated version of the contract:

```solidity
pragma solidity ^0.8.0;

contract SymbolShadowingFixed {
    uint256 public value;

    constructor(uint256 _value) {
        value = _value; // Use a different variable name to avoid shadowing
    }

    function updateValue(uint256 newValue) public {
        value = newValue; // Update the state variable directly
    }

    function getValue() public view returns (uint256) {
        return value; // Return the correct state variable value
    }
}
```

In the `SymbolShadowingFixed` contract, the constructor parameter is renamed to `_value` to avoid shadowing the state variable `value`. This ensures that the state variable is correctly updated and accessed without any unexpected behavior.