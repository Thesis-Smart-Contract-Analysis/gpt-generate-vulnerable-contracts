# Smart contract

```solidity
pragma solidity ^0.4.24;

contract StackSizeLimitVulnerable {
    
    uint256 public result;
    
    function calculate(uint256 input) public {
        if (input == 0) {
            return;
        }
        
        result = input + 1;
        calculate(input - 1);
    }
}
```

The vulnerability lies in the recursive function `calculate` where it keeps calling itself without any termination condition based on the input value. This can lead to a stack overflow if the input value is large, causing the contract to run out of gas and fail.

# Remediations

- Implement a termination condition in the recursive function to prevent stack overflow.
- Use iterative solutions instead of recursive functions for operations that involve potentially large input values.