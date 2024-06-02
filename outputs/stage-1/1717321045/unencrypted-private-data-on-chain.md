# Smart contract

```solidity
pragma solidity ^0.4.24;

contract UnencryptedPrivateData {

  string private sensitiveData;

  function storeData(string _data) public {
    sensitiveData = _data; // Line 6
  }

  function getData() public view returns (string) {
    return sensitiveData; // Line 10
  }
}
```

## Description

The vulnerability in the smart contract `UnencryptedPrivateData` is on lines 6 and 10. The `sensitiveData` variable is declared as private, but the data stored in it is not encrypted. Storing sensitive data in plain text on the blockchain exposes it to anyone who can access the blockchain data.

## Remediations

- Encrypt the sensitive data before storing it on the blockchain using encryption techniques like hashing or encryption algorithms.
- Implement access control mechanisms to restrict who can read or modify the sensitive data.