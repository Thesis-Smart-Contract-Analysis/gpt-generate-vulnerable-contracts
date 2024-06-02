# Smart contract

```solidity
pragma solidity ^0.4.24;

contract IntegerOverflowUnderflow {
    uint public balance = 100;

    function add(uint256 _value) public {
        balance += _value; // Potential Integer Overflow vulnerability here
    }

    function subtract(uint256 _value) public {
        balance -= _value; // Potential Integer Underflow vulnerability here
    }
}
```

Description: The smart contract `IntegerOverflowUnderflow` contains an Integer Overflow vulnerability in the `add` function where the `balance` variable can overflow if a large enough `_value` is added. Similarly, there is an Integer Underflow vulnerability in the `subtract` function where the `balance` variable can underflow if `_value` is greater than the current balance.

# Remediations

- Use SafeMath library from OpenZeppelin to perform arithmetic operations safely.
- Implement checks before performing addition or subtraction to prevent overflow or underflow vulnerabilities.