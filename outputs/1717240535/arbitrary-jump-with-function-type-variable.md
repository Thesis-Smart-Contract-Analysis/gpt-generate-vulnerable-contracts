Below is a vulnerable smart contract that has the Arbitrary Jump with Function Type Variable vulnerability:

```solidity
pragma solidity ^0.8.0;

contract ArbitraryJump {
    address public owner;
    bool public isOwner;

    constructor() {
        owner = msg.sender;
        isOwner = true;
    }

    function arbitraryJump(address _target, bytes memory _data) public {
        require(msg.sender == owner, "Only owner can call this function");
        
        (bool success, ) = _target.call(_data);
        require(success, "Arbitrary jump failed");
    }
}
```

In the `arbitraryJump` function, the owner of the contract can call any function in any contract by passing the target address and data to be executed. This can lead to arbitrary code execution and potential security vulnerabilities.

### Remediation:
To fix the Arbitrary Jump with Function Type Variable vulnerability, you should avoid using `call` with arbitrary data passed as a parameter. Instead, you can implement a whitelist of allowed functions or contracts that the owner can interact with.

Here is an example of how you can remediate the vulnerability:

```solidity
pragma solidity ^0.8.0;

contract FixedArbitraryJump {
    address public owner;
    bool public isOwner;
    mapping(address => bool) public allowedTargets;

    constructor() {
        owner = msg.sender;
        isOwner = true;
    }

    function addAllowedTarget(address _target) public {
        require(msg.sender == owner, "Only owner can add allowed targets");
        allowedTargets[_target] = true;
    }

    function executeFunction(address _target, bytes memory _data) public {
        require(msg.sender == owner, "Only owner can call this function");
        require(allowedTargets[_target], "Target not allowed");

        (bool success, ) = _target.call(_data);
        require(success, "Function execution failed");
    }
}
```

In the remediated contract `FixedArbitraryJump`, the owner can add allowed targets that are safe to interact with. The `executeFunction` function will only execute the function in the allowed targets, preventing arbitrary code execution.