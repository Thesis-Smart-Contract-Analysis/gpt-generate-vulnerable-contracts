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

In the vulnerable smart contract `TODVulnerable`, the `withdraw` function allows a user to withdraw a certain amount of ETH from their balance. However, the vulnerability arises due to the use of `call` to transfer ETH to the `msg.sender`. This can lead to a TOD vulnerability where an attacker can exploit the order of transactions to manipulate the contract state.

### Remediation:

To mitigate the Transaction Ordering Dependency vulnerability, you can follow these best practices:

1. **Use SafeMath Library**: Replace direct arithmetic operations with SafeMath library functions to prevent integer overflow/underflow vulnerabilities.

2. **Avoid External Calls**: Minimize the use of external calls within critical functions to reduce the attack surface. If external calls are necessary, ensure that the contract state is not modified after the external call.

3. **Implement Checks-Effects-Interactions Pattern**: Follow the Checks-Effects-Interactions pattern to ensure that state changes are made before any external calls are executed. This pattern helps prevent reentrancy and TOD vulnerabilities.

4. **Avoid Reliance on Transaction Order**: Design the contract logic in a way that it does not rely on the specific order of transactions. Make the contract state changes independent of the order in which transactions are processed.

Here is an updated version of the smart contract `TODFixed` with the TOD vulnerability remediated:

```solidity
pragma solidity ^0.8.0;

contract TODFixed {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

In the `TODFixed` contract, the state changes are made before the external call, following the Checks-Effects-Interactions pattern to prevent TOD vulnerabilities.