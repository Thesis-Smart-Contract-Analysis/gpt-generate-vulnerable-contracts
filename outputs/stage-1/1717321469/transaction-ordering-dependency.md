# Smart contract with Transaction Ordering Dependency vulnerability

```solidity
pragma solidity ^0.4.24;

contract TransactionOrderingDependency {
  
  uint public balance = 0;

  function deposit() public payable {
    balance += msg.value;
  }

  function withdraw(uint _amount) public {
    require(balance >= _amount);
    msg.sender.transfer(_amount);
    balance -= _amount;
  }

}
```

Description: In the `withdraw` function of the smart contract `TransactionOrderingDependency`, the `balance` is reduced after transferring the funds to the `msg.sender`. This can lead to a Transaction Ordering Dependency vulnerability where an attacker can exploit the order of transactions to withdraw more funds than they should.

# Remediations

- Update the order of operations in the `withdraw` function to first reduce the balance and then transfer the funds to the `msg.sender`.
- Implement a check to ensure that the balance is sufficient before transferring funds to prevent overwithdrawal vulnerabilities.