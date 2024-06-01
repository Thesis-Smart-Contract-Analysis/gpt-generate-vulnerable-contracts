Here is a vulnerable smart contract with Uninitialized Storage Pointer vulnerability:

```solidity
pragma solidity ^0.8.0;

contract UninitializedStoragePointer {
    uint256 public data;

    function setData(uint256 _data) public {
        Data storage newData;
        newData.value = _data;
        data = newData.value;
    }
}
```

In the `setData` function of the smart contract `UninitializedStoragePointer`, the `Data` struct variable `newData` is declared without being initialized. This causes `newData` to act as a storage pointer and point to the storage slot of the `data` variable. As a result, when `_data` is assigned to `newData.value`, it actually modifies the value of the `data` variable in storage.

### Remediation:
To fix the Uninitialized Storage Pointer vulnerability, you should explicitly define the storage location for the `Data` struct variable `newData` as `memory` instead of `storage`. This way, `newData` will be a memory variable and not affect the storage slot of the `data` variable.

Here is the remediated version of the smart contract:

```solidity
pragma solidity ^0.8.0;

contract FixedUninitializedStoragePointer {
    uint256 public data;

    struct Data {
        uint256 value;
    }

    function setData(uint256 _data) public {
        Data memory newData;
        newData.value = _data;
        data = newData.value;
    }
}
```

In the remediated version, the `Data` struct variable `newData` is explicitly defined as a memory variable, ensuring that it does not affect the storage slot of the `data` variable.