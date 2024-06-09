# Smart contract

```solidity
pragma solidity 0.8.0;

contract Token {
    uint public totalSupply = 1000000;
    
    function updateTotalSupply(uint newTotalSupply) public {
        uint totalSupply = newTotalSupply; // Line with Shadowing State Variables vulnerability
    }
}
```

Description of the vulnerability: In the above smart contract, the `updateTotalSupply` function declares a local variable `totalSupply` that shadows the state variable `totalSupply`. This can lead to unexpected behavior as the state variable is not being updated, and the local variable is being modified instead.

# Remediations

- **Remediation 1:** Use a different name for the local variable to avoid shadowing the state variable. For example:
  
  ```solidity
  function updateTotalSupply(uint newTotalSupply) public {
      uint updatedTotalSupply = newTotalSupply;
      totalSupply = updatedTotalSupply;
  }
  ```

- **Remediation 2:** Explicitly reference the state variable when updating its value to ensure clarity and avoid shadowing issues. For example:
  
  ```solidity
  function updateTotalSupply(uint newTotalSupply) public {
      totalSupply = newTotalSupply;
  }
  ```