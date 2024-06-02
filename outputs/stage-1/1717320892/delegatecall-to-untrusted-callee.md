# Smart contract

```solidity
pragma solidity ^0.8.0;

contract VulnerableDelegateCall {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address _newOwner) public {
        owner.delegatecall(abi.encodeWithSignature("setOwner(address)", _newOwner));
    }

    function setOwner(address _newOwner) public {
        require(msg.sender == owner, "Only owner can call this function");
        owner = _newOwner;
    }
}
```

The vulnerability lies in the line:
```solidity
owner.delegatecall(abi.encodeWithSignature("setOwner(address)", _newOwner));
```

# Description

The smart contract `VulnerableDelegateCall` has a vulnerability due to the use of `delegatecall` to call the `setOwner` function of the `owner` address. This allows an attacker to manipulate the state of the contract by calling functions from an untrusted contract.

# Remediations

- Avoid using `delegatecall` to call functions from untrusted contracts.
- Implement proper access control mechanisms to ensure that only authorized users can change critical state variables.