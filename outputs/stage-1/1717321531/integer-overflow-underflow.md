# Smart contract

```solidity
pragma solidity ^0.8.0;

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

Description: The `add` function in the smart contract has a potential Integer Overflow vulnerability as the `balance` variable may exceed its maximum value. Similarly, the `subtract` function has a potential Integer Underflow vulnerability as the `balance` variable may become negative.

# Remediations

- Use SafeMath library to perform arithmetic operations to prevent Integer Overflow/Underflow vulnerabilities.
- Implement checks before performing arithmetic operations to ensure the safety of the calculations.