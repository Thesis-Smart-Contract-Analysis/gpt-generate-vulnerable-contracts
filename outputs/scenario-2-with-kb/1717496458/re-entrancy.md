# Smart Contract with Re-entrancy Vulnerability

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableBank {
    mapping(address => uint256) public balances;

    function deposit() public payable {
        require(msg.value > 0, "Deposit value must be greater than 0");
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 _amount) public {
        uint256 balance = balances[msg.sender];
        require(balance >= _amount, "Insufficient balance");

        (bool sent, ) = msg.sender.call{value: _amount}(""); // Vulnerable line
        require(sent, "Failed to send Ether");

        balances[msg.sender] -= _amount;
    }
}
```

### Description of the Vulnerability
The `withdraw` function in the `VulnerableBank` contract is susceptible to a re-entrancy attack. The vulnerability arises because the contract sends Ether to an external address with `msg.sender.call{value: _amount}("")` before updating the sender's balance. This ordering allows a malicious contract to re-enter the `withdraw` function and potentially withdraw more Ether than the balance if the external contract calls back into `withdraw` during the execution of `msg.sender.call`.

# Remediations

1. **Checks-Effects-Interactions Pattern**: To mitigate re-entrancy attacks, modify the `withdraw` function to follow the Checks-Effects-Interactions pattern. This involves performing all checks first, making all effects (state changes), and only then interacting with other contracts.

    ```solidity
    function withdraw(uint256 _amount) public {
        uint256 balance = balances[msg.sender];
        require(balance >= _amount, "Insufficient balance");

        balances[msg.sender] -= _amount; // State change before external call

        (bool sent, ) = msg.sender.call{value: _amount}("");
        require(sent, "Failed to send Ether");
    }
    ```

2. **Use Reentrancy Guard**: Implement a reentrancy guard to prevent nested (re-entrant) calls to sensitive functions. This can be achieved by using a state variable that locks the contract during the execution of a function.

    ```solidity
    bool private locked = false;

    modifier noReentrant() {
        require(!locked, "No re-entrancy");
        locked = true;
        _;
        locked = false;
    }

    function withdraw(uint256 _amount) public noReentrant {
        uint256 balance = balances[msg.sender];
        require(balance >= _amount, "Insufficient balance");

        balances[msg.sender] -= _amount;

        (bool sent, ) = msg.sender.call{value: _amount}("");
        require(sent, "Failed to send Ether");
    }
    ```

By applying these remediations, the contract can be protected against re-entrancy attacks, ensuring that the state updates are secured before any external interactions that could lead to unexpected re-entries.