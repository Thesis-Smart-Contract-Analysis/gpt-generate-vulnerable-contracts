# Smart contract

```solidity
pragma solidity ^0.8.0;

contract ImmutableBugs {
    address public owner;
    uint public balance;

    constructor() {
        owner = msg.sender;
        balance = 1000;
    }

    function withdraw(uint _amount) public {
        require(msg.sender == owner, "Only owner can withdraw");
        require(balance >= _amount, "Insufficient balance");
        
        balance -= _amount;
        msg.sender.transfer(_amount);
    }
}
```

Description of the vulnerability in the generated smart contract:
The vulnerability in this smart contract lies in the `withdraw` function. Once the contract is deployed, the `balance` variable is initialized to 1000 in the constructor. However, the `balance` can be manipulated by the owner through the `withdraw` function. This means that the owner can potentially drain the entire balance of the contract, leading to loss of funds.

# Remediations

- **Remediation 1:** To fix this vulnerability, you can make the `balance` variable immutable by declaring it as `immutable`. This will prevent the owner from modifying the balance after deployment.
  
- **Remediation 2:** Implement access control mechanisms to restrict who can withdraw funds from the contract. You can use a modifier to check if the caller is the owner before allowing the withdrawal to occur.