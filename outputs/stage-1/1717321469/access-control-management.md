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

## Description

The smart contract `HashForEther` has an Access Control Management vulnerability. The function `withdrawWinnings` does not have an explicit visibility modifier, making its visibility default to `public`. This allows anyone to call the `_sendWinnings` function publicly without any restrictions.

## Remediations

- Add explicit visibility modifiers to functions to control access rights. In this case, you can make the `_sendWinnings` function `internal` to restrict access to within the contract.

```solidity
pragma solidity ^0.4.24;

contract HashForEther {
  
  function withdrawWinnings() public {
    // Winner if the last 8 hex characters of the address are 0.
    require(uint32(msg.sender) == 0);
    _sendWinnings();
  }
  
  function _sendWinnings() internal {
     msg.sender.transfer(this.balance);
  }

}
```