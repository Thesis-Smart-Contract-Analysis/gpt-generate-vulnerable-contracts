# Smart contract

```solidity
pragma solidity ^0.8.0;

contract MaliciousContract {
    address public owner;

    constructor(address _owner) {
        owner = _owner;
    }

    function maliciousFunction() external {
        // Malicious code here
    }
}

contract VulnerableContract {
    address public owner;
    MaliciousContract public maliciousContract;

    constructor(address _owner, address _maliciousContract) {
        owner = _owner;
        maliciousContract = MaliciousContract(_maliciousContract);
    }

    function executeMaliciousFunction() external {
        maliciousContract.maliciousFunction();
    }
}
```

Description of the vulnerability in the generated smart contract:
The vulnerability in this smart contract lies in the `VulnerableContract` contract where an external contract `MaliciousContract` is being instantiated and interacted with. The `maliciousContract` variable is of type `MaliciousContract` and is initialized with an address passed in the constructor. This allows an attacker to deploy a malicious contract and pass its address to the `VulnerableContract`, hiding the fact that it is a malicious contract.

# Remediations

- Use interface to interact with external contracts: Instead of directly instantiating an external contract, define an interface that specifies the functions of the external contract. This way, the `VulnerableContract` can interact with the external contract through the interface without exposing the actual contract implementation.

- Implement access control: Add access control mechanisms to restrict interactions with external contracts to only trusted addresses. This can prevent unauthorized contracts from being used in place of the intended external contract.