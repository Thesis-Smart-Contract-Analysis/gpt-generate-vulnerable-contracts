# Smart contract

```solidity
pragma solidity ^0.4.24;

contract HashForEther {

  function withdrawWinnings() { // Line 7
    // Winner if the last 8 hex characters of the address are 0. 
    require(uint32(msg.sender) == 0);
    _sendWinnings();
  }
  
  function _sendWinnings() { // Line 12
    msg.sender.transfer(this.balance);
  }
     
}
```

## Description

The smart contract `HashForEther` has a Function or State Variable Default Visibility vulnerability. The functions `withdrawWinnings` and `_sendWinnings` do not explicitly specify their visibility, making their visibility default to `public`. This can lead to unintended behavior where functions meant to be internal can be called publicly by anyone.

## Remediations

- Update the visibility of the functions to explicitly specify their visibility. In this case, it is recommended to set the visibility of `withdrawWinnings` to `public` and the visibility of `_sendWinnings` to `internal`.

```solidity
pragma solidity ^0.4.24;

contract HashForEther {
  
  function withdrawWinnings() public { // Explicitly set visibility to public
    // Winner if the last 8 hex characters of the address are 0.
    require(uint32(msg.sender) == 0);
    _sendWinnings();
  }
  
  function _sendWinnings() internal { // Explicitly set visibility to internal
     msg.sender.transfer(this.balance);
  }

}
```