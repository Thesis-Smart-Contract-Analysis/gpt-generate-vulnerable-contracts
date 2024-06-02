# Smart contract

```solidity
pragma solidity ^0.4.24;

contract ArbitraryJump {
    uint256 public data;

    function arbitraryJump(uint256 _value) public {
        if (_value == 1) {
            data = 100;
        } else if (_value == 2) {
            data = 200;
        } else if (_value == 3) {
            data = 300;
        } else if (_value == 4) {
            data = 400;
        } else if (_value == 5) {
            data = 500;
        } else {
            data = 0;
        }
    }
}
```

Description: The `arbitraryJump` function in the smart contract `ArbitraryJump` has an Arbitrary Jump with Function Type Variable vulnerability. Depending on the input `_value`, the function can jump to different parts of the code, potentially leading to unexpected behavior.

# Remediations

- Use a switch-case statement instead of multiple if-else statements to handle different cases more efficiently and securely.
- Implement proper input validation to restrict the possible values of `_value` to prevent arbitrary jumps.