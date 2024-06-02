# Smart contract

```solidity
pragma solidity ^0.8.0;

contract ArbitraryStorage {

    mapping(uint256 => uint256) public data;

    function writeToArbitraryStorage(uint256 _index, uint256 _value) public {
        data[_index] = _value; // Vulnerable line
    }
}
```

The vulnerable line in the smart contract is where the function `writeToArbitraryStorage` writes to the `data` mapping at an arbitrary index specified by `_index`.

# Description

The vulnerability in the smart contract `ArbitraryStorage` lies in the `writeToArbitraryStorage` function where it allows an attacker to write to any storage slot in the `data` mapping by specifying the index `_index`. This can lead to unauthorized modification of critical data stored in the contract's storage.

# Remediations

- **Remediation 1:** Implement access control mechanisms to restrict write access to specific storage slots based on user roles or permissions.
- **Remediation 2:** Use a fixed mapping structure with predefined keys to prevent writing to arbitrary storage locations. Ensure that only authorized functions can modify specific data slots.