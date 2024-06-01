Below is a vulnerable smart contract with Write to Arbitrary Storage Location vulnerability:

```solidity
pragma solidity ^0.8.0;

contract VulnerableStorage {

    mapping(uint256 => uint256) public data;

    function writeToArbitraryStorage(uint256 _index, uint256 _value) public {
        data[_index] = _value;
    }
}
```

In the `VulnerableStorage` contract above, the function `writeToArbitraryStorage` allows anyone to write to any storage location in the `data` mapping by specifying the index `_index` and the value `_value`. This vulnerability can lead to unauthorized modification of critical storage variables, potentially causing unexpected behavior or security breaches.

### Remediation:

To mitigate the Write to Arbitrary Storage Location vulnerability, it is essential to restrict write access to specific storage locations and prevent unauthorized modifications. Here are some remediation steps:

1. **Access Control**: Implement proper access control mechanisms to restrict write access to critical storage variables. Only allow authorized users or contracts to modify storage locations.

2. **Whitelist Approach**: Maintain a whitelist of authorized addresses or contracts that are allowed to write to specific storage locations. Validate the caller's address before allowing write operations.

3. **Use Safe Storage Patterns**: Follow safe storage patterns and avoid direct storage writes in critical functions. Consider using higher-level functions or interfaces to interact with storage variables securely.

4. **Immutable Storage**: Design the contract in a way that critical storage variables are set only once during deployment and cannot be modified afterward. This can prevent unauthorized changes to important data.

By implementing these remediation strategies, you can enhance the security of your smart contract and prevent vulnerabilities related to arbitrary storage writes.