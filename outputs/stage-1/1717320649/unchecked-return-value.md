# Smart contract

```solidity
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

The vulnerability in the smart contract `HashForEther` is in the `withdrawWinnings` function. The function allows anyone to call the `_sendWinnings` function without the required condition being met. This can lead to unauthorized withdrawals of ETH from the smart contract.

## Remediations

- Add explicit visibility to functions to prevent unintended access:
  - Change `function withdrawWinnings()` to `function withdrawWinnings() public`.
  - Change `function _sendWinnings()` to `function _sendWinnings() internal`.