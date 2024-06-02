# Smart contract

```solidity
pragma solidity ^0.4.24;

contract UnencryptedPrivateData {

  string private sensitiveData;

  function storeData(string _data) public {
    sensitiveData = _data; // Line 7
  }

  function getData() public view returns (string) {
    return sensitiveData; // Line 11
  }

}
```

## Description

The vulnerability in the smart contract `UnencryptedPrivateData` is that the `sensitiveData` variable is declared as `private` but is being stored and accessed directly on the blockchain without encryption. This exposes the sensitive data to anyone who can read the blockchain.

## Remediations

- Encrypt the sensitive data before storing it on the blockchain using encryption techniques such as hashing or encryption algorithms.
- Implement access control mechanisms to restrict who can read and write the sensitive data, such as using modifiers or access control functions.