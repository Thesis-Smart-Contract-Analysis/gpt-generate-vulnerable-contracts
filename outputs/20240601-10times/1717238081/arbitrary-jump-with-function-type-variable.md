Below is a vulnerable smart contract that has the Arbitrary Jump with Function Type Variable vulnerability:

```solidity
pragma solidity ^0.8.0;

contract ArbitraryJump {
    address public owner;
    bool public isOwner;

    function ArbitraryJump() public {
        owner = msg.sender;
        isOwner = true;
    }

    function setOwner(address _newOwner) public {
        require(isOwner);
        owner = _newOwner;
    }

    function executeFunction(address _contract, bytes memory _data) public {
        require(msg.sender == owner);
        (bool success, ) = _contract.delegatecall(_data);
        require(success);
    }
}
```

In the `executeFunction` function, the contract allows the owner to delegate call any function in any contract. This can lead to arbitrary code execution and potential security vulnerabilities.

### Remediation:
To fix the Arbitrary Jump with Function Type Variable vulnerability, you should avoid using `delegatecall` with untrusted input. If you need to delegate call a function, make sure to validate the target contract and function being called.

Here is the remediated version of the smart contract:

```solidity
pragma solidity ^0.8.0;

contract SafeArbitraryJump {
    address public owner;
    bool public isOwner;

    constructor() {
        owner = msg.sender;
        isOwner = true;
    }

    function setOwner(address _newOwner) public {
        require(isOwner);
        owner = _newOwner;
    }

    function executeFunction(address _contract, bytes memory _data) public {
        require(msg.sender == owner);
        // Add additional validation to ensure the target contract and function are trusted
        // For example, maintain a whitelist of trusted contracts and functions
        // Only allow delegate call to functions that are pre-approved
        // Implement proper access control mechanisms
        // Perform thorough security audits
    }
}
```

In the remediated version, additional validation and access control mechanisms should be implemented to ensure that only trusted contracts and functions can be called using `delegatecall`. This will help prevent arbitrary code execution and enhance the security of the smart contract.