# Smart contract with Re-entrancy Vulnerability

```solidity
pragma solidity ^0.8.0;

contract ReentrancyVulnerable {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient balance");
        
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "Transfer failed");

        balances[msg.sender] -= _amount;
    }

    function getBalance() public view returns (uint) {
        return balances[msg.sender];
    }
}
```

In the above smart contract, the vulnerability lies in the `withdraw` function where the contract transfers ETH to the caller before updating the balance. This allows a malicious contract to call the `withdraw` function repeatedly before the balance is updated, resulting in a re-entrancy attack.

# Remediations

- Use the Check-Effect-Interaction pattern where you first check conditions, then update state, and finally interact with external contracts.
- Implement a mutex or a state variable to prevent re-entrancy attacks.
- Consider using the OpenZeppelin ReentrancyGuard library to add protection against re-entrancy vulnerabilities.