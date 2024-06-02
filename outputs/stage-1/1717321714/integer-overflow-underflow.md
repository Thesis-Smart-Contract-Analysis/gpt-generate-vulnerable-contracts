# Smart contract

```solidity
pragma solidity ^0.8.0;

contract IntegerOverflowUnderflow {
    uint256 public balance = 100;

    function add(uint256 _value) public {
        balance += _value; // Line with Integer Overflow vulnerability
    }

    function subtract(uint256 _value) public {
        balance -= _value; // Line with Integer Underflow vulnerability
    }
}
```

Description of the vulnerability in the above smart contract:
The vulnerability in the smart contract `IntegerOverflowUnderflow` is on the lines where the `balance` variable is modified. In the `add` function, there is an Integer Overflow vulnerability where adding a large value to `balance` can cause it to wrap around and become a very small number. In the `subtract` function, there is an Integer Underflow vulnerability where subtracting a value larger than the current balance can result in an unexpected large positive value.

# Remediations

- Use SafeMath library to perform arithmetic operations to prevent Integer Overflow/Underflow vulnerabilities.
- Implement checks before performing arithmetic operations to ensure the values won't cause overflow or underflow.