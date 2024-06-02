# Smart contract

```solidity
pragma solidity ^0.8.0;

contract VulnerableDelegateCall {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address _newOwner) public {
        require(msg.sender == owner);
        (bool success, ) = _newOwner.delegatecall(abi.encodeWithSignature("setOwner(address)", _newOwner));
        require(success);
    }

    function setOwner(address _newOwner) public {
        owner = _newOwner;
    }
}
```

In the above smart contract, the vulnerability lies in the line:

```solidity
(bool success, ) = _newOwner.delegatecall(abi.encodeWithSignature("setOwner(address)", _newOwner));
```

This line uses `delegatecall` to call the `setOwner` function of an untrusted address `_newOwner`. This allows the untrusted callee to modify the state variables of the `VulnerableDelegateCall` contract, potentially leading to unauthorized changes in ownership.

# Remediations

- **Remediation 1**: Avoid using `delegatecall` to call functions of untrusted addresses. Ensure that only trusted contracts are allowed to modify critical state variables.
- **Remediation 2**: Implement access control mechanisms to restrict which addresses can call functions that modify sensitive state variables.
- **Remediation 3**: Use a whitelist approach to validate the addresses that can be called using `delegatecall` to prevent unauthorized modifications.