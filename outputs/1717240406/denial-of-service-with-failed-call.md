Below is a vulnerable smart contract that has Denial of Service with Failed Call vulnerability:

```solidity
pragma solidity ^0.8.0;

contract DenialOfService {
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

    function () external payable {
        while (true) {
            deposit(); // Repeatedly deposit to consume all gas
        }
    }
}
```

In the `DenialOfService` contract above, the fallback function is designed to consume all gas by repeatedly depositing funds into the contract. This can lead to a Denial of Service attack where legitimate users are unable to interact with the contract due to the continuous consumption of gas.

### Remediation:

To mitigate the Denial of Service with Failed Call vulnerability, you can implement a gas limit check in the fallback function to prevent excessive gas consumption. Here is an updated version of the contract with the remediation:

```solidity
pragma solidity ^0.8.0;

contract DenialOfServiceFixed {
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

    function () external payable {
        require(gasleft() > 2300, "Insufficient gas");
        while (true) {
            deposit(); // Repeatedly deposit to consume all gas
        }
    }
}
```

In the remediated `DenialOfServiceFixed` contract, a gas limit check is added to the fallback function to ensure that the gas remaining is sufficient before executing the deposit loop. This prevents the contract from consuming all gas and allows legitimate transactions to go through.

By implementing this gas limit check, the contract can prevent the Denial of Service attack with Failed Call vulnerability.