Sure! Here is a vulnerable smart contract with Uninitialized Storage Pointer vulnerability:

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

In the `setData` function of the `UninitializedStoragePointer` contract, the `Data` struct variable `newData` is declared without being initialized. This causes `newData` to point to the storage slot of the `data` variable, potentially leading to unintended changes in the state variables.

### Remediation:

To fix the Uninitialized Storage Pointer vulnerability, you should explicitly initialize the struct variable before using it. Here is the remediated version of the smart contract:

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

In the remediated version, the `Data` struct variable `newData` is explicitly initialized with the `_data` value before being used, ensuring that it does not point to unintended storage slots.