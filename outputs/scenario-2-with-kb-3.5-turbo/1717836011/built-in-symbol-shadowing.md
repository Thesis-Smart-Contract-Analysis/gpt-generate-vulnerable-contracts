# Smart contract

```solidity
pragma solidity ^0.8.0;

contract BuiltInSymbolShadowing {
    
    uint256 msg; // Overshadows built-in message variable.

    function block() public view returns (uint256) {
        return block.number; // Overshadows built-in block function.
    }

}
```

Description of the vulnerability in the above smart contract:

The vulnerability in the smart contract is the Built-in Symbol Shadowing issue. In this contract, the variable `msg` overshadows the built-in `msg` variable, and the function `block` overshadows the built-in `block` function. This can lead to unexpected behavior and potential security risks.

# Remediations

- Rename the variable `msg` to something that does not conflict with built-in variables or functions, such as `userMsg`.
- Rename the function `block` to a different name that does not conflict with built-in functions, such as `getBlockNumber`.