# Smart contract

```solidity
pragma solidity ^0.8.0;

contract IntegerOverflowVulnerable {
  
    uint public count = 1;

    function run(uint256 input) public {
        count -= input; // Vulnerability: Integer Underflow here
    }
    
}
```

## Description

The vulnerable smart contract `IntegerOverflowVulnerable` contains an Integer Underflow vulnerability on the line where the subtraction operation `count -= input;` is performed. If the `input` value is greater than the current value of `count`, an underflow will occur, leading to unexpected results and potential security risks.

## Remediations

- **Remediation 1:** Implement SafeMath library or similar safe arithmetic operations to prevent integer overflow/underflow vulnerabilities. Using SafeMath ensures that arithmetic operations are checked for overflows and underflows before execution, thus safeguarding against such vulnerabilities.

- **Remediation 2:** Upgrade the Solidity version to 0.8.0 or higher, where automatic overflow checks are enforced by the compiler. In Solidity 0.8.0 and above, transactions causing overflows or underflows will revert before the operation is executed, providing built-in protection against such vulnerabilities.