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

The vulnerability in the smart contract `HashForEther` is related to the Access Control Management. The function `_sendWinnings` is not explicitly defined with a visibility specifier, making its visibility default to `public`. This means that anyone can call the `_sendWinnings` function and withdraw ETH from the smart contract without the intended restriction based on the last 8 hex characters of the sender's address.

## Remediations

- Explicitly define the visibility specifier for functions to ensure proper access control. In this case, you can change the visibility of the `_sendWinnings` function to `internal` to restrict access to within the contract.

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