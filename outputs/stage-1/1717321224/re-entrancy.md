# Smart contract with Re-entrancy vulnerability

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

    function attack(address _target) public payable {
        (bool success, ) = _target.call{value: msg.value}("");
        require(success, "Attack failed");
        
        withdraw(msg.value);
    }

    receive() external payable {}
}
```

## Description

In the `ReentrancyVulnerable` smart contract above, the `withdraw` function allows a user to withdraw a specified amount of ETH from their balance. However, the vulnerability lies in the fact that the `withdraw` function performs the ETH transfer before updating the user's balance. This allows a malicious contract to call the `withdraw` function recursively before the balance is updated, resulting in a re-entrancy attack.

## Remediations

- Implement the Check-Effect-Interaction pattern where you first check conditions, then update state variables, and finally interact with external contracts.
- Use the Withdrawal Pattern where users need to withdraw their funds instead of automatically transferring funds in the same function.
- Consider using the OpenZeppelin ReentrancyGuard library to protect against re-entrancy attacks.