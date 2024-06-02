# Smart contract

```solidity
pragma solidity >=0.4.0 < 0.6.0;

contract FloatingCompilerVersion {
  
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

The vulnerability lies in the floating compiler version specified in the pragma statement.

# Description

The smart contract `FloatingCompilerVersion` has a vulnerability related to the floating compiler version specified in the pragma statement. By allowing a range of compiler versions, the contract can be compiled using different compiler versions, potentially leading to unexpected behavior or vulnerabilities.

# Remediations

- Specify a fixed compiler version in the pragma statement to ensure consistency and avoid potential vulnerabilities.
- Update the pragma statement to a specific Solidity version, for example: `pragma solidity 0.5.16;`.

By fixing the compiler version, you ensure that the smart contract is compiled consistently and reduces the risk of vulnerabilities arising from using different compiler versions.