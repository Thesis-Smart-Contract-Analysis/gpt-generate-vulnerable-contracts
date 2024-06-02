# Smart contract

```solidity
/*
 * @source: https://github.com/sigp/solidity-security-blog#visibility
 * @author: SigmaPrime 
 * Modified by Gerhard Wagner
 */

pragma solidity ^0.4.24;

contract HashForEther {

  function withdrawWinnings() { // Line 7
    // Winner if the last 8 hex characters of the address are 0. 
    require(uint32(msg.sender) == 0);
    _sendWinnings();
  }
  
  function _sendWinnings() { // Line 13
    msg.sender.transfer(this.balance);
  }
     
}
```

## Description

The vulnerability in the smart contract `HashForEther` lies in the default visibility of the functions. The functions `withdrawWinnings` and `_sendWinnings` have default visibility, which is `public`. This means that these functions can be called by anyone externally, potentially leading to unintended behavior.

## Remediations

- Explicitly specify the visibility of functions to prevent unintended external access. In this case, change the visibility of the functions to `public` and `internal` respectively.

```solidity
/*
 * @source: https://github.com/sigp/solidity-security-blog#visibility
 * @author: SigmaPrime
 * Modified by Gerhard Wagner
 */

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

By explicitly specifying the visibility of the functions, we ensure that only the intended access is allowed, enhancing the security of the smart contract.