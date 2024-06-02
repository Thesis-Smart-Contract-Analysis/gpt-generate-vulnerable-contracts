# Smart contract

```solidity
pragma solidity ^0.8.0;

contract VulnerableContract {
    mapping(address => uint) balances;

    function withdraw(uint _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient balance");
        
        (bool success, ) = msg.sender.call{value: _amount}("");
        if (success) {
            balances[msg.sender] -= _amount;
        }
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
}
```

Description of the vulnerability in the generated smart contract:
The vulnerability in the `withdraw` function lies in the external call to `msg.sender.call{value: _amount}("")`. This external call allows an attacker to re-enter the `withdraw` function before the previous call completes, potentially leading to a re-entrancy attack.

# Remediations

- Use the Checks-Effects-Interactions pattern: Reorder the code in the `withdraw` function to first update the state variables, then interact with external contracts. This prevents re-entrancy attacks by ensuring that state changes are completed before any external calls.
- Implement a withdrawal pattern: Instead of directly sending Ether to `msg.sender`, consider using a withdrawal pattern where users can withdraw their funds in a separate function. This separation of concerns can help mitigate re-entrancy vulnerabilities.