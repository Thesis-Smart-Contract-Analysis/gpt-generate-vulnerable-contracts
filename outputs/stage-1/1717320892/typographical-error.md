# Smart contract

```solidity
pragma solidity ^0.4.24;

contract HashForEther {

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

The Typographical Error vulnerability is in the line:
```solidity
require(uint32(msg.sender) == 0);
```

Description: The `withdrawWinnings` function in the `HashForEther` contract has a Typographical Error vulnerability. The intention seems to be to check if the last 8 hex characters of the sender's address are 0, but the code mistakenly uses `uint32(msg.sender)` which actually converts the entire address to a `uint32` before comparison.

# Remediations

- Explicitly extract the last 8 hex characters of the sender's address for comparison.
- Use bitwise operations or string manipulation to correctly check the last 8 hex characters of the address.