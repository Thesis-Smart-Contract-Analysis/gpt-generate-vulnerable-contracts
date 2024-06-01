Below is a vulnerable smart contract that has the Message Call with Hardcoded Gas Amount vulnerability:

```solidity
pragma solidity ^0.8.0;

contract MessageCallVulnerable {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferFunds(address payable _recipient, uint _amount) public {
        require(msg.sender == owner, "Only the owner can transfer funds");
        
        // Vulnerable message call with hardcoded gas amount
        (bool success, ) = _recipient.call{value: _amount, gas: 50000}("");
        require(success, "Transfer failed");
    }
}
```

In the `transferFunds` function of the smart contract `MessageCallVulnerable`, there is a vulnerable message call using `call` with a hardcoded gas amount of 50,000. Hardcoding the gas amount in a message call can lead to unexpected behavior, especially if the gas provided is not sufficient for the operation to be completed successfully.

### Remediation:

To remediate the vulnerability, it is recommended to avoid hardcoding gas amounts in message calls. Instead, use the `gas` parameter dynamically based on the gas available in the transaction. Here is an updated version of the smart contract with the vulnerability remediated:

```solidity
pragma solidity ^0.8.0;

contract MessageCallFixed {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferFunds(address payable _recipient, uint _amount) public {
        require(msg.sender == owner, "Only the owner can transfer funds");
        
        // Fixed message call with dynamic gas amount
        (bool success, ) = _recipient.call{value: _amount, gas: gasleft()}("");
        require(success, "Transfer failed");
    }
}
```

In the remediated version, the `gas` parameter in the message call is set dynamically using `gasleft()`, which returns the amount of gas left for the current transaction. This ensures that the message call has enough gas to complete the operation successfully without hardcoding a specific gas amount.