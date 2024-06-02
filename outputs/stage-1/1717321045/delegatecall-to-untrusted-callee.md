# Smart contract

```solidity
pragma solidity ^0.8.0;

contract VulnerableDelegateCall {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address _newOwner) public {
        owner.delegatecall(abi.encodeWithSignature("setOwner(address)", _newOwner)); // Vulnerable line
    }

    function setOwner(address _newOwner) public {
        require(msg.sender == owner, "Only owner can call this function");
        owner = _newOwner;
    }
}
```

Description of the vulnerability in the above smart contract:
The vulnerability lies in the `transferOwnership` function where it uses `delegatecall` to call the `setOwner` function of the `owner` address. This allows an attacker to manipulate the storage of the `VulnerableDelegateCall` contract by calling the `setOwner` function of a malicious contract.

# Remediations

- Use `call` instead of `delegatecall` to interact with external contracts to prevent unintended storage manipulation.
- Implement access control mechanisms to ensure that only authorized users can change the owner of the contract.