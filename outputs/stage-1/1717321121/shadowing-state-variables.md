# Smart contract

```solidity
pragma solidity ^0.4.24;

contract ShadowingStateVariables {
    uint public num = 10; // line 5

    function updateNum(uint _num) public {
        uint num = _num; // line 9
        num = _num * 2;
    }
}
```

Description: In the smart contract `ShadowingStateVariables`, there is a Shadowing State Variables vulnerability on line 9. The local variable `num` declared inside the function `updateNum` shadows the state variable `num`, causing potential confusion and unintended behavior.

# Remediations

- Explicitly differentiate between state variables and local variables by using a naming convention such as prefixing state variables with `this.` or using a different naming convention.
- Avoid reusing variable names to prevent shadowing and improve code clarity.