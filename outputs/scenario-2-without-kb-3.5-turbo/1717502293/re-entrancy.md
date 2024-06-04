# Smart contract with Re-entrancy vulnerability

```solidity
pragma solidity ^0.8.0;

contract VulnerableContract {
    mapping(address => uint) balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient balance");
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "Transfer failed");
        balances[msg.sender] -= _amount;
    }

    function maliciousWithdraw(address _victim, uint _amount) public {
        (bool success, ) = _victim.call(abi.encodeWithSignature("withdraw(uint256)", _amount));
        require(success, "Malicious transfer failed");
    }
}
```

Description of the vulnerability in the generated smart contract:
The vulnerability lies in the `withdraw` function where the contract allows the caller to withdraw a specified amount of funds. However, the `withdraw` function does not update the sender's balance before transferring the funds. This allows an attacker to repeatedly call the `withdraw` function before the balance is updated, resulting in a re-entrancy attack.

# Remediations

- **Update State Before External Calls**: Ensure that the state variables are updated before making any external calls. In this case, move the deduction of the withdrawn amount from the sender's balance to before the external call to prevent re-entrancy attacks.

- **Use the Checks-Effects-Interactions Pattern**: Follow the Checks-Effects-Interactions pattern where you first perform all checks, then update the state, and finally interact with external contracts. This pattern helps prevent re-entrancy vulnerabilities by separating state changes from external calls.