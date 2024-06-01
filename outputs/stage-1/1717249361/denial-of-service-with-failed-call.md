Below is a vulnerable smart contract that has Denial of Service with Failed Call vulnerability:

```solidity
pragma solidity ^0.8.0;

contract DenialOfService {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdrawAll() public {
        uint amount = balances[msg.sender];
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        balances[msg.sender] = 0;
    }
}
```

In the `withdrawAll` function of the smart contract `DenialOfService`, the `call` function is used to send Ether to the `msg.sender`. However, if the `call` fails (for example, if the gas stipend provided is not enough), the `require(success)` will revert the transaction, but the `balances[msg.sender]` will still be set to 0. This can lead to a denial of service attack where an attacker can repeatedly call the `withdrawAll` function to drain the contract's balance and set the balances to 0.

### Remediation:

To prevent the Denial of Service with Failed Call vulnerability, you can implement the following remediation:

1. **Use Transfer Method**: Instead of using `call`, use the `transfer` method which automatically reverts the transaction if the transfer fails. This ensures that the state changes are reverted if the transfer fails.

2. **Check Return Value**: If you need to use `call` for more complex scenarios, always check the return value of the `call` to handle failures gracefully. You can implement a pattern like Check-Effect-Interaction to ensure that state changes are only applied if the call was successful.

Here is the remediated version of the smart contract using the `transfer` method:

```solidity
pragma solidity ^0.8.0;

contract DenialOfServiceFixed {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdrawAll() public {
        uint amount = balances[msg.sender];
        require(amount > 0, "Insufficient balance");
        balances[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}
```

In the remediated version, the `withdrawAll` function uses the `transfer` method to send Ether to the `msg.sender`. This ensures that if the transfer fails, the transaction will be reverted, and the state changes will not be applied. Additionally, the balance check is done before transferring the funds to prevent draining the contract balance without sufficient funds.