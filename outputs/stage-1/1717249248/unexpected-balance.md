Below is a vulnerable smart contract that exhibits the Unexpected Balance vulnerability:

```solidity
pragma solidity ^0.8.0;

contract VulnerableContract {
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

In the `withdraw` function of the `VulnerableContract`, the contract allows users to withdraw a specified amount of Ether from their balance. However, the vulnerability lies in the use of `msg.sender.call{value: amount}("")` to transfer Ether. This method of transferring Ether can lead to unexpected behavior if the recipient address is a contract with a fallback function that performs unexpected operations.

### Remediation:
To mitigate the Unexpected Balance vulnerability, it is recommended to use the `transfer` or `send` functions for transferring Ether instead of `call`. These functions provide better security as they only forward a fixed amount of gas and do not execute any code on the receiving contract.

Here is the remediated version of the smart contract using `transfer`:

```solidity
pragma solidity ^0.8.0;

contract FixedContract {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }
}
```

In the remediated version, the `withdraw` function uses `payable(msg.sender).transfer(amount)` to transfer the specified amount of Ether to the sender. This approach is safer and reduces the risk of unexpected behavior due to the transfer of Ether.