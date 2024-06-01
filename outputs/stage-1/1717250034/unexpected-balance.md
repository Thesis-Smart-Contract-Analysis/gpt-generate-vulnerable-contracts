Below is a vulnerable smart contract that exhibits the Unexpected Balance vulnerability:

```solidity
pragma solidity ^0.8.0;

contract UnexpectedBalance {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        payable(msg.sender).transfer(amount);
        balances[msg.sender] -= amount;
    }

    function getContractBalance() public view returns (uint) {
        return address(this).balance;
    }
}
```

In the `UnexpectedBalance` smart contract, the `deposit` function allows users to deposit Ether into their account. The `withdraw` function allows users to withdraw a specified amount of Ether from their account. However, there is a vulnerability in the `withdraw` function where the balance is deducted before the transfer is made. This can lead to unexpected behavior if the transfer fails, leaving the user's balance deducted without receiving the Ether.

### Remediation:
To fix the Unexpected Balance vulnerability, the deduction of the balance should only occur after a successful transfer of Ether. Here is the remediated version of the smart contract:

```solidity
pragma solidity ^0.8.0;

contract FixedUnexpectedBalance {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        uint balanceBeforeTransfer = balances[msg.sender];
        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
        assert(balances[msg.sender] == balanceBeforeTransfer - amount);
    }

    function getContractBalance() public view returns (uint) {
        return address(this).balance;
    }
}
```

In the remediated `FixedUnexpectedBalance` smart contract, the balance deduction is moved after the transfer to ensure that the user's balance is only deducted if the transfer is successful. Additionally, an `assert` statement is used to verify that the balance deduction was done correctly.

By making these changes, the vulnerability of Unexpected Balance is mitigated, and users can safely withdraw their funds without the risk of losing their balance unexpectedly.