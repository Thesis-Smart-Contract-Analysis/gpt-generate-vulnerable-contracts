# Smart Contract

```solidity
pragma solidity ^0.8.0;

contract ArbitraryStorageWrite {
    uint256 public criticalValue = 100;

    function writeStorage(uint256 index, uint256 value) public {
        assembly {
            sstore(index, value)
        }
    }
}
```

In the above smart contract, the vulnerability exists in the `writeStorage` function. This function allows anyone to write to any storage slot in the contract directly by specifying the `index` and `value`. This can lead to unauthorized modifications of critical contract variables, such as `criticalValue`.

# Remediations

1. **Restrict Access**: Ensure that only authorized addresses can call sensitive functions that modify storage. This can be implemented using access control mechanisms such as the `Ownable` pattern from OpenZeppelin, where only the owner of the contract can perform certain operations.

    ```solidity
    pragma solidity ^0.8.0;

    import "@openzeppelin/contracts/access/Ownable.sol";

    contract ArbitraryStorageWriteSafe is Ownable {
        uint256 public criticalValue = 100;

        function writeStorage(uint256 index, uint256 value) public onlyOwner {
            assembly {
                sstore(index, value)
            }
        }
    }
    ```

2. **Remove Unsafe Assembly**: Avoid using low-level assembly code that directly interacts with the contract's storage unless absolutely necessary. Instead, use Solidity's high-level constructs which are safer and less prone to errors.

    ```solidity
    pragma solidity ^0.8.0;

    contract ArbitraryStorageWriteSafer {
        uint256 public criticalValue = 100;

        function updateCriticalValue(uint256 newValue) public {
            criticalValue = newValue;
        }
    }
    ```

By implementing these remediations, the contract can be protected against unauthorized modifications and potential vulnerabilities associated with direct storage access.