Below is a vulnerable smart contract that has the Write to Arbitrary Storage Location vulnerability:

```solidity
pragma solidity ^0.8.0;

contract VulnerableStorage {

    mapping(uint256 => uint256) public data;

    function writeToArbitraryStorage(uint256 _index, uint256 _value) public {
        data[_index] = _value;
    }
}
```

In the `VulnerableStorage` contract above, the function `writeToArbitraryStorage` allows anyone to write to any storage location in the `data` mapping by specifying the index `_index` and the value `_value`. This vulnerability can lead to unauthorized modification of critical storage variables, potentially causing unexpected behavior or security risks.

### Remediation:

To mitigate the Write to Arbitrary Storage Location vulnerability, it is essential to restrict write access to specific storage locations and prevent unauthorized modifications. Here are some remediation steps:

1. **Access Control**: Implement proper access control mechanisms to restrict write access to critical storage variables. Only allow authorized users or contracts to modify storage locations.

2. **Whitelist Approach**: Maintain a whitelist of authorized addresses or contracts that are allowed to write to specific storage locations. Validate the caller's address before allowing any write operations.

3. **Use Safe Storage Patterns**: Follow secure storage patterns such as Check-Effect-Interaction to ensure that storage modifications are performed safely and securely.

Here is an example of how the `VulnerableStorage` contract can be remediated to address the vulnerability:

```solidity
pragma solidity ^0.8.0;

contract SecureStorage {

    mapping(uint256 => uint256) private data;
    address private owner;

    constructor() {
        owner = msg.sender;
    }

    function writeToSecureStorage(uint256 _index, uint256 _value) public {
        require(msg.sender == owner, "Unauthorized access");
        data[_index] = _value;
    }

    function readFromSecureStorage(uint256 _index) public view returns (uint256) {
        return data[_index];
    }
}
```

In the `SecureStorage` contract above, access control is implemented by allowing only the contract owner to write to the storage locations. The `writeToSecureStorage` function checks if the caller is the owner before allowing any modifications. This approach ensures that only authorized entities can write to the storage locations, mitigating the vulnerability.