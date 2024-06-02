# Smart contract with Function Selector Clashing vulnerability

```solidity
pragma solidity ^0.8.0;

contract FunctionSelectorClash {
    
    function transfer(address _to, uint _amount) public {
        // Transfer tokens to the specified address
    }
    
    function transfer(uint _amount, address _to) public {
        // Transfer tokens to the specified address
    }
    
}
```

In the above smart contract, the vulnerability lies in having two functions with the same name `transfer` but with different parameter order. This can lead to confusion for external callers and may result in unexpected behavior.

# Remediations

- Use unique function names to avoid function selector clashes.
- Ensure that functions with the same name have different parameter types or order to prevent ambiguity.