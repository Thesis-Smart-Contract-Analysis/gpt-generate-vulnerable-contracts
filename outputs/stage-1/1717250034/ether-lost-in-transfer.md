Below is a vulnerable smart contract that has the Ether Lost in Transfer vulnerability:

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
    
    receive() external payable {}
}
```

In the `EtherTransfer` smart contract above, the `transferEther` function allows the owner to transfer all the Ether stored in the contract to a specified recipient address. However, there is a vulnerability in this function that can lead to Ether Lost in Transfer.

### Vulnerability Description:
- The `transferEther` function transfers all the Ether stored in the contract to the specified recipient address without checking if the transfer was successful.
- If the transfer fails (for example, if the recipient address is a contract with a fallback function that consumes too much gas), the Ether will be lost in the transfer.

### Remediation:
To prevent the Ether Lost in Transfer vulnerability, you can implement the following remediation steps:

1. Check the return value of the `transfer` function to ensure the transfer was successful:
   - Use the return value of the `transfer` function to handle any potential errors that may occur during the transfer.
   - Revert the transaction if the transfer fails to prevent Ether loss.

Here is the updated `transferEther` function with the remediation applied:

```solidity
function transferEther(address payable _recipient) public {
    require(msg.sender == owner, "Only the owner can transfer Ether");
    uint256 balanceToSend = address(this).balance;
    (bool success, ) = _recipient.call{value: balanceToSend}("");
    require(success, "Ether transfer failed");
}
```

By checking the return value of the `call` function after the transfer, you can ensure that the Ether transfer is successful and handle any errors appropriately.

Implementing this remediation will help prevent the Ether Lost in Transfer vulnerability in the smart contract.