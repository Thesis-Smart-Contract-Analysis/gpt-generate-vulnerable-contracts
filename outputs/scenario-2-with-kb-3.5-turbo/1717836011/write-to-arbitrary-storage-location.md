# Smart contract

```solidity
pragma solidity ^0.8.0;

contract ArbitraryStorage {
    mapping(uint256 => uint256) data;

    function writeToArbitraryStorage(uint256 _index, uint256 _value) public {
        data[_index] = _value; // Vulnerable line
    }
}
```

Description of the vulnerability in the above smart contract:

The vulnerability in the smart contract `ArbitraryStorage` lies in the `writeToArbitraryStorage` function where it allows any user to write to arbitrary storage locations using the `_index` parameter without proper access control. This can lead to unauthorized modification of sensitive data stored in the contract.

# Remediations

- Implement Access Control: Ensure that only authorized users or contracts can write to specific storage locations. Use modifiers or require statements to enforce access control based on roles or permissions.
- Use Safe Storage Patterns: Utilize secure storage patterns such as separating critical data into different contracts or using mappings with carefully controlled keys to prevent unauthorized writes to arbitrary storage locations.