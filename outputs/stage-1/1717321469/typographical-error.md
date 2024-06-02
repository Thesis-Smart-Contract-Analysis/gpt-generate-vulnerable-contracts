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

The Typographical Error vulnerability is in line 6 of the smart contract where the function `withdrawWinnings` is missing the visibility specifier.

# Description

In the `withdrawWinnings` function, the visibility specifier for the function is missing, which defaults the visibility to `public`. This can lead to unintended behavior where external parties can call internal functions of the smart contract publicly.

# Remediations

- Add the visibility specifier `public` to the `withdrawWinnings` function to explicitly define the visibility.

```solidity
pragma solidity ^0.4.24;

contract TypoFixed {
  
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