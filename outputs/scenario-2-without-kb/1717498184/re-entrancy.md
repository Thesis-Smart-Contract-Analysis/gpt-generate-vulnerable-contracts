# Smart Contract with Re-entrancy Vulnerability

Here is an example of a simple smart contract written in Solidity that demonstrates a re-entrancy vulnerability:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableBank {
    mapping(address => uint256) public balances;

    function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than 0");
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient balance");

        (bool sent, ) = msg.sender.call{value: _amount}(""); // Vulnerable line
        require(sent, "Failed to send Ether");

        balances[msg.sender] -= _amount;
    }

    receive() external payable {}
}
```

### Description of the Vulnerability in the Generated Smart Contract

The vulnerability in this contract lies in the `withdraw` function, specifically at the line where `msg.sender.call{value: _amount}("")` is called. This line sends Ether to the caller before deducting the amount from the caller's balance. An attacker can exploit this by creating a malicious contract that calls `withdraw` recursively before the original `withdraw` call completes. This can lead to multiple withdrawals being made while the balance is only reduced once, potentially draining the contract's funds.

# Remediations

To fix the re-entrancy vulnerability in the `VulnerableBank` contract, consider the following remediations:

- **Remediation 1: Checks-Effects-Interactions Pattern**
  Implement the Checks-Effects-Interactions pattern. This means you should make all state changes before calling external contracts. Here's how you can adjust the `withdraw` function:

  ```solidity
  function withdraw(uint256 _amount) public {
      require(balances[msg.sender] >= _amount, "Insufficient balance");

      balances[msg.sender] -= _amount; // State change before interaction

      (bool sent, ) = msg.sender.call{value: _amount}("");
      require(sent, "Failed to send Ether");
  }
  ```

- **Remediation 2: Use `transfer` or `send` Instead of `call`**
  The `call` method forwards all available gas by default, which can lead to vulnerabilities. Using `transfer` (which forwards only 2300 gas and reverts on failure) or `send` (which returns a boolean) can prevent re-entrancy in some cases:

  ```solidity
  function withdraw(uint256 _amount) public {
      require(balances[msg.sender] >= _amount, "Insufficient balance");

      balances[msg.sender] -= _amount;

      // Using transfer instead of call
      payable(msg.sender).transfer(_amount);
  }
  ```

  Note that while `transfer` and `send` are safer against re-entrancy, they are not recommended for all use cases due to gas limitations and potential future changes in Ethereum.

- **Remediation 3: Reentrancy Guard**
  Use a reentrancy guard modifier that prevents nested (reentrant) calls to functions marked by this modifier:

  ```solidity
  bool private locked = false;

  modifier noReentrancy() {
      require(!locked, "No reentrancy allowed");
      locked = true;
      _;
      locked = false;
  }

  function withdraw(uint256 _amount) public noReentrancy {
      require(balances[msg.sender] >= _amount, "Insufficient balance");
      balances[msg.sender] -= _amount;

      (bool sent, ) = msg.sender.call{value: _amount}("");
      require(sent, "Failed to send Ether");
  }
  ```

Implementing any of these remediations will help mitigate the risk of re-entrancy attacks on the `VulnerableBank` contract.