Below is a vulnerable smart contract that has the Write to Arbitrary Storage Location vulnerability:

```solidity
pragma solidity ^0.8.0;

contract WriteToArbitraryStorage {
    mapping(uint256 => uint256) public data;

    function writeToStorage(uint256 _index, uint256 _value) public {
        data[_index] = _value;
    }

    function writeArbitraryStorage(uint256 _index, uint256 _value) public {
        bytes32 slot = keccak256(abi.encodePacked(_index));
        assembly {
            sstore(slot, _value)
        }
    }
}
```

In the `writeArbitraryStorage` function, the contract uses inline assembly to directly write to an arbitrary storage slot based on the `_index` provided by the caller. This can lead to unauthorized modification of storage slots and potentially compromise the integrity of the contract.

### Remediation:

To mitigate the Write to Arbitrary Storage Location vulnerability, you should avoid using inline assembly to directly write to storage slots based on user-provided input. Instead, you can implement a secure storage pattern where storage slots are managed in a controlled manner.

Here is an example of how you can refactor the vulnerable contract to use a secure storage pattern:

```solidity
pragma solidity ^0.8.0;

contract SecureStoragePattern {
    mapping(uint256 => uint256) private data;

    function writeToStorage(uint256 _index, uint256 _value) public {
        require(_index < 100, "Index out of bounds");
        data[_index] = _value;
    }

    function readFromStorage(uint256 _index) public view returns (uint256) {
        require(_index < 100, "Index out of bounds");
        return data[_index];
    }
}
```

In the refactored contract, the `writeToStorage` function ensures that the `_index` provided by the caller is within a predefined range to prevent writing to arbitrary storage locations. Additionally, the `data` mapping is now private to restrict direct access to storage slots.

By following this secure storage pattern and validating input parameters, you can prevent unauthorized writes to arbitrary storage locations and enhance the security of your smart contract.