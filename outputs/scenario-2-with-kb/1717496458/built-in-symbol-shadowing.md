# Smart Contract with Built-in Symbol Shadowing Vulnerability

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ShadowingExample {
    uint public now = block.timestamp; // line 6: Built-in Symbol Shadowing

    function setNow(uint _now) public {
        now = _now;
    }
}
```

### Description of the Vulnerability in the Above Smart Contract
In the provided smart contract, the state variable `now` shadows the built-in global variable `now` in Solidity, which is an alias for `block.timestamp`. This can lead to confusion and errors in the contract, as the semantic meaning of `now` is overridden, potentially leading to misuse in the contract logic where `block.timestamp` was intended to be used.

# Remediations

1. **Rename the State Variable**: To avoid shadowing and ensure clarity in the contract code, rename the state variable `now` to a more descriptive and unique name that does not conflict with any built-in global variables. For example, `currentTimestamp` or `contractTimestamp` could be used.

2. **Use Explicit References**: When intending to use the built-in `block.timestamp`, always refer to it explicitly as `block.timestamp` instead of `now`. This practice prevents any ambiguity and makes the code more readable and maintainable, especially in larger codebases or when multiple developers are involved.

By implementing these remediations, the smart contract code becomes clearer and safer, reducing the risk of bugs related to misunderstanding the purpose and value of the `now` variable.