# Smart contract

```solidity
pragma solidity ^0.8.0;

contract UncheckedReturnValue {
    
    address public owner;

    function transferOwnership(address _newOwner) public {
        owner = _newOwner;
    }

    function callTransferOwnership(address _contract, address _newOwner) public {
        (bool success, ) = _contract.delegatecall(abi.encodeWithSignature("transferOwnership(address)", _newOwner));
        require(success); // Line with Unchecked Return Value vulnerability
    }
}
```

Description: The `callTransferOwnership` function in the smart contract `UncheckedReturnValue` uses `delegatecall` to call the `transferOwnership` function of another contract without checking the return value for success. This can lead to unexpected behavior if the delegatecall fails but the contract continues execution.

# Remediations

- Use `success` variable to check the return value of the `delegatecall` and handle any failure appropriately.
- Implement proper error handling mechanisms to revert the transaction if the `delegatecall` fails.