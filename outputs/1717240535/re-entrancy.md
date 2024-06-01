Below is a vulnerable smart contract with Re-entrancy vulnerability:

```solidity
pragma solidity ^0.8.0;

contract VulnerableContract {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        balances[msg.sender] -= amount;
    }

    function attack(address _target) public payable {
        (bool success, ) = _target.call{value: msg.value}("");
        require(success, "Attack failed");
        
        withdraw(msg.value);
    }

    fallback() external payable {
        if (msg.sender != address(this)) {
            withdraw(msg.value);
        }
    }
}
```

In this vulnerable smart contract, the `withdraw` function allows a user to withdraw a certain amount of ETH from their balance. The `attack` function is used to exploit the vulnerability by calling the `withdraw` function recursively during the fallback function.

### Remediation for Re-entrancy Vulnerability:

To prevent Re-entrancy vulnerability, you can follow these remediation steps:

1. **Use the Checks-Effects-Interactions Pattern**: Ensure that all state changes are made before interacting with external contracts. This pattern helps in preventing re-entrancy attacks.

2. **Implement a Withdrawal Pattern**: Separate the state changes from the transfer of funds. Update the user's balance first and then transfer the funds to the user.

3. **Use the `nonReentrant` Modifier**: Implement a `nonReentrant` modifier to prevent a function from being called recursively.

Here is an updated version of the smart contract with the remediation applied:

```solidity
pragma solidity ^0.8.0;

contract SecureContract {
    mapping(address => uint) public balances;
    mapping(address => bool) private _locked;

    modifier nonReentrant() {
        require(!_locked[msg.sender], "Re-entrancy attack detected");
        _locked[msg.sender] = true;
        _;
        _locked[msg.sender] = false;
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public nonReentrant {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        balances[msg.sender] -= amount;
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

In the updated version, the `nonReentrant` modifier is used to prevent re-entrancy attacks by locking the function during execution. This ensures that the function cannot be called recursively by the same address.