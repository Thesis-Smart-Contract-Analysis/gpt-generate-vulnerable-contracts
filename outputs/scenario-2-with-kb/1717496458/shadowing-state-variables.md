# Smart Contract

```solidity
pragma solidity ^0.8.0;

contract BaseContract {
    uint256 public value = 100;
}

contract DerivedContract is BaseContract {
    uint256 public value = 200;  // Line 7: Shadowing State Variable 'value'
}

```

## Description of the Vulnerability in the Above Smart Contract

In the provided Solidity code, the `DerivedContract` inherits from `BaseContract`. Both contracts declare a public state variable named `value`. In Solidity, this leads to a situation known as "shadowing" where the `value` in `DerivedContract` shadows or overrides the `value` in `BaseContract`. This can cause confusion and errors in contract behavior because the `value` variable in `DerivedContract` does not actually override the `value` in `BaseContract` in the way typical method overriding works in object-oriented programming. Instead, it declares a new state variable unique to `DerivedContract`, potentially leading to unexpected behavior if the contract's logic assumes `value` is shared or overridden across the inheritance chain.

# Remediations

1. **Explicit Override with `override` Keyword (Solidity 0.6.0 and above):**
   To address shadowing and make it clear that a state variable is meant to override a variable in a base contract, Solidity 0.6.0 introduced the `override` keyword for functions. However, for state variables, overriding is not directly supported. The recommended approach is to avoid re-declaring the variable in the derived contract and use setter functions to modify its value if needed.

2. **Use Setter Function in Base Contract:**
   Modify the base contract to include setter and getter functions for the state variable, and use these functions in the derived contract to manipulate the value. This approach avoids direct access and manipulation of state variables and adheres to the principle of encapsulation.

   ```solidity
   pragma solidity ^0.8.0;

   contract BaseContract {
       uint256 private value = 100;

       function setValue(uint256 _value) public {
           value = _value;
       }

       function getValue() public view returns (uint256) {
           return value;
       }
   }

   contract DerivedContract is BaseContract {
       function updateValue(uint256 _newValue) public {
           setValue(_newValue);
       }
   }
   ```

   In this revised version, `DerivedContract` uses `setValue()` to change the `value`, ensuring that there is no shadowing and the logic related to `value` is centrally managed in `BaseContract`. This approach enhances maintainability and clarity of the code.