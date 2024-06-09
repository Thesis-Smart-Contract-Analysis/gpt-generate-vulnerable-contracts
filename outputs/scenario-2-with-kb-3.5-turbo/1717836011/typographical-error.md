# Smart contract

```solidity
pragma solidity ^0.8.0;

contract TypoIncorrectComparison {
  uint public targetNumber = 10;
  uint public userInput;

  function isNumberEqual() public view returns (bool) {
    return userInput = targetNumber;
  }
}
```

Description of the vulnerability in the above smart contract:

In the `isNumberEqual` function, the comparison operator `=` is used instead of the equality comparison operator `==`. This means that instead of checking if `userInput` is equal to `targetNumber`, the function assigns the value of `targetNumber` to `userInput` and then returns `true`. This unintended behavior can lead to unexpected results and security vulnerabilities.

# Remediations

- Use the correct equality comparison operator `==` to compare values in the `isNumberEqual` function.
- Implement proper input validation to ensure that the smart contract behaves as intended and to prevent unintended assignments like in the vulnerable code.