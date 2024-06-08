# Smart contract

```solidity
pragma solidity ^0.8.0;

contract UncheckedReturnValue {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address _newOwner) public {
        (bool success, ) = _newOwner.call(abi.encodeWithSignature("setOwner(address)", _newOwner));
        if (success) {
            owner = _newOwner;
        }
    }
}
```

Description of the vulnerability in the above smart contract:

The vulnerability lies in the `transferOwnership` function where the return value of the `call` function is not checked. If the `setOwner` function call to the new owner address fails, the `owner` variable is still updated without verification, potentially leading to unexpected behavior.

# Remediations

- **Remediation 1:** Check the return value of the `call` function to ensure the success of the external call before updating the state variables.

```solidity
function transferOwnership(address _newOwner) public {
    (bool success, ) = _newOwner.call(abi.encodeWithSignature("setOwner(address)", _newOwner));
    require(success, "External call failed");
    owner = _newOwner;
}
```

- **Remediation 2:** Implement a more robust error handling mechanism to handle failures in external calls gracefully, such as reverting the transaction if the call fails.

```solidity
function transferOwnership(address _newOwner) public {
    (bool success, ) = _newOwner.call(abi.encodeWithSignature("setOwner(address)", _newOwner));
    require(success, "External call failed");
    owner = _newOwner;
}
```