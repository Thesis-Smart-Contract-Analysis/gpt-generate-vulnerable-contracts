Below is a vulnerable smart contract that has the Message Call with Hardcoded Gas Amount vulnerability:

```solidity
pragma solidity ^0.8.0;

contract MessageCallVulnerable {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferEther(address payable _recipient, uint _amount) public {
        require(msg.sender == owner, "Only the owner can transfer Ether");
        
        // Vulnerability: Hardcoded gas amount in the call
        (bool success, ) = _recipient.call{value: _amount, gas: 100000}("");
        require(success, "Transfer failed");
    }
}
```

In the `transferEther` function, there is a hardcoded gas amount of 100,000 specified in the `call` function. This can lead to issues if the gas required for the execution of the recipient contract's fallback function exceeds the hardcoded gas amount, resulting in a failed transfer.

### Remediation:
To fix the vulnerability, you should avoid hardcoding gas amounts in `call` functions. Instead, you can use `gasleft()` to dynamically determine the remaining gas and pass it to the `call` function. Here is the remediated version of the smart contract:

```solidity
pragma solidity ^0.8.0;

contract MessageCallFixed {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferEther(address payable _recipient, uint _amount) public {
        require(msg.sender == owner, "Only the owner can transfer Ether");
        
        // Remediation: Dynamically determine the gas amount
        uint gasLimit = gasleft();
        (bool success, ) = _recipient.call{value: _amount, gas: gasLimit}("");
        require(success, "Transfer failed");
    }
}
```

By using `gasleft()` to dynamically determine the remaining gas, you ensure that the recipient contract's fallback function has enough gas to execute successfully. This helps prevent the vulnerability associated with hardcoded gas amounts in message calls.