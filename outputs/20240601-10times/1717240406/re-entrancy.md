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

    function attack(address vulnerableContractAddress) public payable {
        (bool success, ) = vulnerableContractAddress.call{value: msg.value}("");
        require(success, "Attack failed");
        
        withdraw(msg.value);
    }

    receive() external payable {}
}
```

In this vulnerable smart contract, the `withdraw` function allows a user to withdraw a certain amount of ETH from their balance. The `attack` function is designed to exploit the Re-entrancy vulnerability by calling the `withdraw` function after transferring ETH to the vulnerable contract.

### Remediation for Re-entrancy Vulnerability:

To remediate the Re-entrancy vulnerability, you can follow these best practices:

1. **Use the Check-Effect-Interaction Pattern**: Ensure that state changes are made before interacting with external contracts. This pattern helps prevent re-entrancy attacks by first checking conditions, then updating state variables, and finally interacting with external contracts.

2. **Implement a Withdrawal Pattern**: Separate the withdrawal logic from the state update to prevent re-entrancy attacks. Transfer the ETH to the user before updating the balance.

3. **Use the Withdrawal Pattern with Checks-Effects-Interactions**: Implement a withdrawal pattern where the user initiates the withdrawal and then the contract sends the ETH. This pattern ensures that the state is updated before sending the ETH.

Here is an example of how you can modify the `withdraw` function to prevent Re-entrancy:

```solidity
function withdraw(uint amount) public {
    require(balances[msg.sender] >= amount, "Insufficient balance");
    
    balances[msg.sender] -= amount;
    
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

By updating the state variable `balances` before interacting with external contracts, you can prevent the Re-entrancy vulnerability in your smart contract.