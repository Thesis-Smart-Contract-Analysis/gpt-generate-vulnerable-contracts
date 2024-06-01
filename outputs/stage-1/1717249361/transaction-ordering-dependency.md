Below is a vulnerable smart contract with Transaction Ordering Dependency (TOD) vulnerability:

```solidity
pragma solidity ^0.8.0;

contract TODVulnerable {
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
}
```

In the vulnerable smart contract `TODVulnerable`, the `withdraw` function allows users to withdraw funds from their balance. However, the vulnerability arises when an attacker exploits the TOD vulnerability by performing the following steps:
1. The attacker deposits a certain amount of Ether into the contract.
2. The attacker then calls the `withdraw` function to withdraw the deposited amount.
3. Before the transaction is confirmed, the attacker performs another action that changes the state of the contract (e.g., depositing more Ether or calling another function).
4. The attacker's second transaction is confirmed before the `withdraw` transaction, allowing the attacker to manipulate the contract state and potentially exploit the vulnerability.

### Remediation:

To mitigate the Transaction Ordering Dependency vulnerability, you can implement a reentrancy guard using the OpenZeppelin ReentrancyGuard library. This guard prevents reentrancy attacks and ensures that the contract state is not manipulated by external calls during the execution of critical functions.

Here is the remediated version of the smart contract using the ReentrancyGuard:

```solidity
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract TODFixed is ReentrancyGuard {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public nonReentrant {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        balances[msg.sender] -= amount;
    }
}
```

In the remediated smart contract `TODFixed`, the `withdraw` function is modified to use the `nonReentrant` modifier from the ReentrancyGuard library. This modifier prevents reentrancy attacks by ensuring that the function is not called recursively or reentrantly.

By implementing the ReentrancyGuard, you can effectively mitigate the Transaction Ordering Dependency vulnerability and secure the contract against potential exploits.