Below is a vulnerable smart contract with Re-entrancy vulnerability:

```solidity
pragma solidity ^0.8.0;

contract VulnerableContract {
    mapping(address => uint) private balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        balances[msg.sender] -= amount;
    }

    function getBalance() public view returns (uint) {
        return balances[msg.sender];
    }

    function attack(address vulnerableContractAddress) public payable {
        (bool success, ) = vulnerableContractAddress.call{value: msg.value}("");
        require(success, "Attack failed");
        
        withdraw(msg.value);
    }
}
```

In this vulnerable smart contract, the `withdraw` function allows a user to withdraw a certain amount of ETH from their balance. The vulnerability arises when the `withdraw` function is called by an attacker's contract in a re-entrant manner. The attacker's contract can repeatedly call the `withdraw` function before the balance is updated, allowing the attacker to drain the contract's balance.

### Remediation for Re-entrancy Vulnerability:

To remediate the Re-entrancy vulnerability, you can follow the Check-Effect-Interaction pattern and use a mutex to prevent re-entrancy. Here is an updated version of the smart contract with the remediation:

```solidity
pragma solidity ^0.8.0;

contract SecureContract {
    mapping(address => uint) private balances;
    mapping(address => bool) private locked;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        require(!locked[msg.sender], "Withdrawal in progress");

        locked[msg.sender] = true;
        
        balances[msg.sender] -= amount;
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Transfer failed");

        locked[msg.sender] = false;
    }

    function getBalance() public view returns (uint) {
        return balances[msg.sender];
    }
}
```

In the remediated version of the smart contract:
1. A `locked` mapping is introduced to keep track of whether a withdrawal is in progress for a specific address.
2. Before processing a withdrawal, the contract checks if the address is not already in the locked state to prevent re-entrancy.
3. The contract sets the `locked` state to true before processing the withdrawal and resets it to false after the withdrawal is completed.

By implementing the Check-Effect-Interaction pattern and using a mutex, the remediated smart contract prevents re-entrancy attacks by ensuring that a withdrawal cannot be re-entered until the previous withdrawal is completed.