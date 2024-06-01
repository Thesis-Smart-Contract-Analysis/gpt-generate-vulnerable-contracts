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

In the `writeToArbitraryStorage` function of the `VulnerableStorage` contract, the user can specify the index `_index` where they want to write the value `_value` in the `data` mapping. This allows an attacker to write to any storage location within the `data` mapping, potentially causing unexpected behavior or manipulation of critical data.

### Remediation:

To mitigate the Write to Arbitrary Storage Location vulnerability, you should avoid allowing users to directly specify the storage location they want to write to. Instead, you can implement a more controlled approach by using a whitelist of allowed storage locations or by restricting write operations to specific predefined storage slots.

Here is an example of how you can remediate the vulnerability:

```solidity
pragma solidity ^0.8.0;

contract SecureStorage {

    mapping(uint256 => uint256) public data;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function writeToSpecificStorage(uint256 _index, uint256 _value) public {
        require(msg.sender == owner, "Only the owner can write to storage");
        require(_index < 10, "Index out of bounds"); // Limiting storage writes to specific slots
        data[_index] = _value;
    }
}
```

In the `SecureStorage` contract, the `writeToSpecificStorage` function restricts write operations to specific storage slots by checking if the index `_index` is within a predefined range (in this case, 0 to 9). Additionally, only the owner of the contract can perform write operations to ensure control over storage writes.