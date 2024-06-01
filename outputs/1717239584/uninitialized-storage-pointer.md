Below is a vulnerable smart contract with Uninitialized Storage Pointer vulnerability:

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

In the `setData` function of the smart contract `UninitializedStoragePointer`, the `Data` struct variable `newData` is declared without being initialized. This causes `newData` to act as a storage pointer and point to an arbitrary storage slot, potentially leading to unintended changes in storage variables.

### Remediation:
To fix the Uninitialized Storage Pointer vulnerability, you should explicitly initialize the `Data` struct variable `newData` before using it. Here is the remediated version of the smart contract:

```solidity
pragma solidity ^0.8.0;

contract FixedUninitializedStoragePointer {
    uint256 public data;

    struct Data {
        uint256 value;
    }

    function setData(uint256 _data) public {
        Data storage newData = Data(_data);
        data = newData.value;
    }
}
```

In the remediated version, the `Data` struct variable `newData` is initialized with the `_data` value before assigning it to the `data` variable. This ensures that `newData` is not acting as an uninitialized storage pointer.