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
    
    function depositEther() public payable {
        // Function to deposit Ether
    }
}
```

In the `transferEther` function, the contract transfers all its Ether balance to the `_recipient` address. This can lead to Ether loss if the recipient address is a contract with a fallback function that consumes more gas than the gas stipend provided by the `transfer` function.

### Remediation:
To prevent Ether Lost in Transfer vulnerability, you can implement the following remediation:

1. **Use `send` or `revert` Pattern**: Instead of using `transfer`, use the `send` method along with checking the return value to handle the failure of the transfer. If the transfer fails, revert the transaction to prevent Ether loss.

2. **Implement Withdrawal Pattern**: Implement a withdrawal pattern where users can withdraw their funds instead of transferring all Ether to an external address in a single transaction.

3. **Limit Gas Usage**: If you still want to use `transfer`, ensure that the recipient address is a trusted address or contract that does not consume excessive gas in its fallback function.

Here is an updated version of the smart contract with the remediation applied:

```solidity
pragma solidity ^0.8.0;

contract EtherTransferFixed {
    
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    function transferEther(address payable _recipient) public {
        require(msg.sender == owner, "Only the owner can transfer Ether");
        (bool success, ) = _recipient.call{value: address(this).balance}("");
        require(success, "Transfer failed");
    }
    
    function depositEther() public payable {
        // Function to deposit Ether
    }
}
```

In the remediated version, the `transferEther` function now uses the `call` method to send Ether to the recipient address and checks the success status of the transfer. If the transfer fails, the transaction will be reverted to prevent Ether loss.