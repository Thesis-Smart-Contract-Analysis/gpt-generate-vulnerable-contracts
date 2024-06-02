# Smart contract

```solidity
pragma solidity ^0.4.24;

contract TypoVulnerable {
  
  function withdrawWinnings() {
    // Winner if the last 8 hex characters of the address are 0. 
    require(uint32(msg.sender) == 0);
    _sendWinnings();
  }
  
  function _sendWinnings() {
    msg.sender.transfer(this.balance);
  }
     
}
```

The Typographical Error vulnerability is in the line `require(uint32(msg.sender) == 0);` of the `withdrawWinnings` function.

# Description

In the `withdrawWinnings` function, the intention is to check if the last 8 hex characters of the sender's address are all zeros to determine the winner. However, due to a typographical error, the code incorrectly converts the sender's address to a `uint32` and checks if it equals zero. This check will not accurately verify the last 8 hex characters of the address.

# Remediations

- Explicitly convert the sender's address to a `uint32` to extract the last 8 hex characters for comparison.
- Use bitwise operations to extract the last 8 hex characters of the sender's address for accurate comparison.