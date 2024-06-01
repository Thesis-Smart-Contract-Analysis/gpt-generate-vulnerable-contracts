Below is a vulnerable smart contract with Uninitialized Storage Pointer vulnerability:

```solidity
pragma solidity ^0.8.0;

contract UninitializedStoragePointer {
    uint256 public data;

    function setData(uint256 _data) public {
        UninitializedStruct uninitializedStruct;
        uninitializedStruct.num = _data;
        data = uninitializedStruct.num;
    }

    struct UninitializedStruct {
        uint256 num;
    }
}
```

In the `setData` function of the `UninitializedStoragePointer` contract, the `UninitializedStruct uninitializedStruct` variable is declared but not initialized. When trying to access the `num` field of this uninitialized struct, it points to the storage slot of the contract's state variable `data`. This can lead to unexpected behavior and manipulation of the contract's state.

### Remediation:
To fix the Uninitialized Storage Pointer vulnerability, you should explicitly initialize the struct variable before accessing its fields. Here is the remediated version of the smart contract:

```solidity
pragma solidity ^0.8.0;

contract FixedUninitializedStoragePointer {
    uint256 public data;

    function setData(uint256 _data) public {
        UninitializedStruct memory uninitializedStruct = UninitializedStruct(_data);
        data = uninitializedStruct.num;
    }

    struct UninitializedStruct {
        uint256 num;
    }
}
```

In the remediated version, the `UninitializedStruct` variable is explicitly initialized with the `_data` value before accessing its `num` field. This ensures that the struct is properly initialized before usage, eliminating the Uninitialized Storage Pointer vulnerability.