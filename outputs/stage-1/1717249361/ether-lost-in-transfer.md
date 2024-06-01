Below is a vulnerable smart contract with Ether Lost in Transfer vulnerability:

```solidity
pragma solidity ^0.8.0;

contract EtherTransfer {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferEther(address payable _recipient) public {
        require(msg.sender == owner, "Only the owner can transfer Ether");
        _recipient.transfer(address(this).balance);
    }
}
```

In the `EtherTransfer` smart contract above, the `transferEther` function allows the owner to transfer all the Ether stored in the contract to a specified recipient address. However, there is a vulnerability in this function that can lead to Ether loss.

### Vulnerability:
If the recipient address provided in the `transferEther` function is a smart contract with a fallback function that consumes more than 2300 gas, the transfer will fail, and the Ether will be lost in the process.

### Remediation:
To prevent Ether loss in transfer, you can use the `send` or `call` method instead of `transfer` and implement proper error handling. Here is the updated version of the `transferEther` function with remediation:

```solidity
function transferEther(address payable _recipient) public {
    require(msg.sender == owner, "Only the owner can transfer Ether");
    (bool success, ) = _recipient.call{value: address(this).balance}("");
    require(success, "Transfer failed");
}
```

In the remediated version, we use the `call` method with explicit gas and value parameters. We also check the return value of the `call` to ensure the transfer was successful. This way, if the transfer fails, the contract will revert the transaction and prevent Ether loss.