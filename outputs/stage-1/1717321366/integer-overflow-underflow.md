# Smart contract

```solidity
pragma solidity ^0.4.24;

contract IntegerOverflowUnderflow {
    uint256 public balance = 100;

    function add(uint256 _value) public {
        balance += _value; // Potential Integer Overflow vulnerability here
    }

    function subtract(uint256 _value) public {
        balance -= _value; // Potential Integer Underflow vulnerability here
    }
}
```

Description of the vulnerability in the above smart contract:
The `add` function has an Integer Overflow vulnerability where the `balance` can exceed the maximum value that a `uint256` can hold. Similarly, the `subtract` function has an Integer Underflow vulnerability where the `balance` can become negative if `_value` is greater than the current `balance`.

# Remediations

- Use SafeMath library from OpenZeppelin to perform arithmetic operations safely.
- Implement checks to ensure that the arithmetic operations do not result in overflow or underflow.