# Smart contract

```solidity
pragma solidity ^0.4.24;

contract ShadowingStateVariables {
    uint public num = 10; // line 5

    function updateNum(uint _num) public {
        uint num = _num; // line 8
        num = _num * 2;
    }
}
```

Description of the vulnerability in the above smart contract:
The vulnerability in the smart contract `ShadowingStateVariables` is on line 8 where a local variable `num` is declared inside the function `updateNum` with the same name as the state variable `num`. This causes shadowing, where the local variable `num` takes precedence over the state variable `num` within the function, potentially leading to unintended behavior or confusion.

# Remediations

- Use different variable names for local variables to avoid shadowing state variables.
- Be mindful of naming conventions to clearly distinguish between state variables and local variables.