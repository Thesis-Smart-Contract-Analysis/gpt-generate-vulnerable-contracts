# Smart contract

```solidity
pragma solidity >=0.4.0 < 0.6.0;

contract FloatingCompilerVersion {
  
}
```

## Description

The smart contract `FloatingCompilerVersion` has a vulnerability related to the floating compiler version pragma statement. The pragma statement allows the contract to be compiled by multiple compiler versions within the specified range, which can lead to inconsistencies in testing and deployment environments.

## Remediations

- Specify a fixed compiler version in the pragma statement to ensure consistent compilation across different environments.
- Update the pragma statement to a specific version, for example: `pragma solidity 0.5.16;`.

By fixing the compiler version, you can avoid potential issues related to floating compiler versions.