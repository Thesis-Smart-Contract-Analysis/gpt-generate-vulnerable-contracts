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

    fallback() external payable {
        if (msg.sender != address(this)) {
            withdraw(msg.value);
        }
    }
}
```

## Description

In the `ReentrancyVulnerable` smart contract above, the `withdraw` function allows a user to withdraw a specified amount of ETH from their balance. However, the function does not update the user's balance before transferring the ETH, which can lead to a re-entrancy vulnerability. An attacker can call the `attack` function, which in turn calls the `withdraw` function of another target address. If the target address is a malicious contract that calls back into the `ReentrancyVulnerable` contract before the balance is updated, the attacker can repeatedly withdraw funds without decrementing their balance.

## Remediations

- Ensure that state changes are made before any external calls, especially transfers of ETH.
- Implement a check-effect-interaction pattern where state changes are made before interacting with external contracts.
- Consider using the Withdrawal Pattern to separate the state update and the transfer of funds to prevent re-entrancy attacks.