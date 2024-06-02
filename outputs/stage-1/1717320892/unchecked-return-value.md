# Smart contract

```solidity
pragma solidity ^0.8.0;

contract UncheckedReturnValue {
    
    address public owner;

    function transferOwnership(address _newOwner) public {
        owner = _newOwner;
    }

    function changeOwner(address _newOwner) public {
        owner.call(abi.encodeWithSignature("transferOwnership(address)", _newOwner));
    }
}
```

The vulnerability lies in the line `owner.call(abi.encodeWithSignature("transferOwnership(address)", _newOwner));` where the return value of the `call` function is not checked.

# Remediations

- Use `bool success = owner.call(abi.encodeWithSignature("transferOwnership(address)", _newOwner));` to capture the return value of the `call` function and then check `require(success)` to ensure the call was successful.
- Implement a mechanism to handle the return value appropriately, such as reverting the transaction if the call fails.

By implementing these remediations, you can mitigate the Unchecked Return Value vulnerability in the smart contract.