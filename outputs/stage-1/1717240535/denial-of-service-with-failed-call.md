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

In the `withdrawAll` function, the contract attempts to transfer the entire balance of the caller to the caller's address using a low-level call. If the call fails (for example, if the recipient's fallback function consumes too much gas), the `require(success, "Transfer failed")` statement will revert the transaction, but the gas used for the failed call is not refunded. An attacker can repeatedly call the `withdrawAll` function, causing a denial of service by consuming all the gas.

### Remediation:

To mitigate the Denial of Service with Failed Call vulnerability, you can implement a withdrawal pattern where the user initiates the withdrawal and the contract sends the funds to the user instead of relying on a low-level call. Here is an updated version of the smart contract with the remediation:

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
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }

    function withdraw(uint amount) public {
        require(amount > 0 && amount <= balances[msg.sender], "Invalid amount");
        balances[msg.sender] -= amount;
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

In the remediated version, the `withdrawAll` function now checks if the user has a non-zero balance before attempting the transfer. Additionally, a new `withdraw` function is added to allow users to specify the amount they want to withdraw, providing more control over the withdrawal process.

By implementing this withdrawal pattern, the vulnerability of Denial of Service with Failed Call can be mitigated.