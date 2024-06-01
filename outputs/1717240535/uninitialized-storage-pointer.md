Sure! Here is a vulnerable smart contract with Uninitialized Storage Pointer vulnerability:

```solidity
pragma solidity ^0.8.0;

contract UninitializedStoragePointer {
    uint256 public data;

    function setData(uint256 _data) public {
        DataRecord newRecord;
        newRecord.data = _data;
        data = newRecord.data;
    }
}

struct DataRecord {
    uint256 data;
}
```

In the `setData` function of the `UninitializedStoragePointer` contract, the `DataRecord` struct variable `newRecord` is not initialized before assigning a value to its `data` field. This can lead to the `newRecord` variable pointing to uninitialized storage slots, potentially causing unexpected behavior or security vulnerabilities.

### Remediation:
To fix the Uninitialized Storage Pointer vulnerability, you should explicitly initialize the `DataRecord` struct variable before assigning values to its fields. Here is the remediated version of the smart contract:

```solidity
pragma solidity ^0.8.0;

contract FixedUninitializedStoragePointer {
    uint256 public data;

    function setData(uint256 _data) public {
        DataRecord memory newRecord = DataRecord(_data);
        data = newRecord.data;
    }
}

struct DataRecord {
    uint256 data;
}
```

In the remediated version, the `newRecord` variable is explicitly initialized with the `_data` value before assigning it to the `data` field. This ensures that the storage pointer is properly initialized and avoids the Uninitialized Storage Pointer vulnerability.