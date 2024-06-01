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

In the vulnerable smart contract `TODVulnerable`, the `withdraw` function allows a user to withdraw a certain amount of ETH from their balance. However, the vulnerability arises when an attacker can exploit the order of transactions to manipulate the balance and withdraw more ETH than they actually have.

The attacker can perform the following steps to exploit the vulnerability:
1. The attacker deposits a certain amount of ETH into the contract.
2. Before the deposit transaction is confirmed, the attacker calls the `withdraw` function with an amount greater than their actual balance.
3. The `withdraw` function checks the balance at the time of the call, which is lower than the actual balance due to the pending deposit transaction.
4. The attacker's withdrawal is successful, allowing them to withdraw more ETH than they should be able to.

## Remediation

To mitigate the Transaction Ordering Dependency vulnerability, you can implement a check to ensure that the balance is updated correctly before allowing a withdrawal. One common approach is to use a withdrawal pattern where the user initiates a withdrawal and the contract holds the funds until the withdrawal is confirmed.

Here is an updated version of the smart contract with a remediation:

```solidity
pragma solidity ^0.8.0;

contract TODFixed {
    mapping(address => uint) public balances;
    mapping(address => uint) public pendingWithdrawals;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        pendingWithdrawals[msg.sender] += amount;
    }

    function completeWithdrawal() public {
        uint amount = pendingWithdrawals[msg.sender];
        require(amount > 0, "No pending withdrawal");
        require(address(this).balance >= amount, "Contract balance too low");

        pendingWithdrawals[msg.sender] = 0;
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

In the `TODFixed` smart contract, the `withdraw` function now stores the withdrawal amount in a `pendingWithdrawals` mapping. The user can then call the `completeWithdrawal` function to finalize the withdrawal after ensuring that the balance is correct. This pattern helps prevent the TOD vulnerability by separating the withdrawal process into two steps and ensuring the correct order of operations.