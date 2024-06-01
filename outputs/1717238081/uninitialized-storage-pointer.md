Here is a vulnerable smart contract with Uninitialized Storage Pointer vulnerability:

```solidity
pragma solidity ^0.8.0;

contract UninitializedStoragePointer {
    uint256 public data;

    function setData(uint256 _data) public {
        DataRecord newRecord;
        newRecord.data = _data;
        data = newRecord.data;
    }

    struct DataRecord {
        uint256 data;
    }
}
```

In the `setData` function of the smart contract `UninitializedStoragePointer`, the `DataRecord` struct variable `newRecord` is not initialized before assigning a value to its `data` field. This can lead to the `newRecord` variable pointing to uninitialized storage slots, potentially causing unexpected behavior or security vulnerabilities.

### Remediation:
To remediate the Uninitialized Storage Pointer vulnerability in the smart contract, you should explicitly initialize the `DataRecord` struct variable `newRecord` before assigning a value to its `data` field. Here is the remediated version of the smart contract:

```solidity
pragma solidity ^0.8.0;

contract FixedUninitializedStoragePointer {
    uint256 public data;

    function setData(uint256 _data) public {
        DataRecord memory newRecord = DataRecord(_data);
        data = newRecord.data;
    }

    struct DataRecord {
        uint256 data;
        
        constructor(uint256 _data) {
            data = _data;
        }
    }
}
```

In the remediated version, the `DataRecord` struct variable `newRecord` is explicitly initialized with the provided data before assigning it to the `data` field. Additionally, a constructor is added to the `DataRecord` struct to ensure proper initialization of the struct when creating a new instance.