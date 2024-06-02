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

Description: The `withdrawWinnings` function in the `HashForEther` contract has a Typographical Error vulnerability. The intention was to check if the last 8 hex characters of the sender's address are 0, but the code mistakenly checks if the first 4 bytes of the sender's address are 0 instead.

# Remediations

- Update the `withdrawWinnings` function to correctly check the last 8 hex characters of the sender's address:
```solidity
function withdrawWinnings() public {
    // Winner if the last 8 hex characters of the address are 0.
    require(uint256(msg.sender) % 2**32 == 0);
    _sendWinnings();
}
```

By making this change, the function will correctly check the last 8 hex characters of the sender's address for the condition.