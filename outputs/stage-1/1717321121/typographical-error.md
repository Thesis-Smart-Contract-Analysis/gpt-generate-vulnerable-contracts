# Smart contract with Typographical Error Vulnerability

```solidity
pragma solidity ^0.8.0;

contract TypoVulnerable {
  
  uint256 public balance = 1000;

  function withdraw(uint256 _amount) public {
    require(msg.sender == tx.origin);
    balance -= _amount;
    msg.sender.transfer(_amount);
  }

}
```

## Description

In the smart contract `TypoVulnerable` above, there is a Typographical Error vulnerability in the `withdraw` function. The line `require(msg.sender == tx.origin);` is intended to ensure that the original sender of the transaction is the one calling the `withdraw` function. However, there is a typo in `tx.origin` where it should be `msg.sender`.

## Remediation

- Change `require(msg.sender == tx.origin);` to `require(msg.sender == msg.sender);` to fix the Typographical Error vulnerability.