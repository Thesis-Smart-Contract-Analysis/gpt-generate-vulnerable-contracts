Below is a vulnerable smart contract that exhibits the Insufficient Gas Griefing vulnerability:

```solidity
pragma solidity ^0.8.0;

contract GasGriefing {
    address public owner;
    uint public balance;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address _newOwner) public {
        require(msg.sender == owner, "Only the owner can transfer ownership");
        owner = _newOwner;
    }

    function withdraw(uint _amount) public {
        require(msg.sender == owner, "Only the owner can withdraw funds");
        require(_amount <= balance, "Insufficient balance");
        
        // Vulnerable code: Revert without consuming all gas
        revert("Withdrawal reverted");
    }
}
```

In the `withdraw` function of the `GasGriefing` contract, the contract reverts with a message without consuming all the gas available. This can be exploited by an attacker to perform a griefing attack by repeatedly calling the `withdraw` function with a small amount of gas, causing the owner to waste gas fees without actually withdrawing any funds.

### Remediation:
To mitigate the Insufficient Gas Griefing vulnerability, you can update the `withdraw` function to consume all available gas before reverting. One common approach is to use a gas stipend to forward the remaining gas to a trusted contract or address before reverting. Here is an example of how you can remediate the vulnerability:

```solidity
pragma solidity ^0.8.0;

contract GasGriefingFixed {
    address public owner;
    uint public balance;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address _newOwner) public {
        require(msg.sender == owner, "Only the owner can transfer ownership");
        owner = _newOwner;
    }

    function withdraw(uint _amount) public {
        require(msg.sender == owner, "Only the owner can withdraw funds");
        require(_amount <= balance, "Insufficient balance");
        
        // Consume all gas before reverting
        address payable trustedAddress = payable(owner);
        selfdestruct(trustedAddress);
    }
}
```

In the remediated `withdraw` function, the contract forwards all remaining gas to the owner's address using `selfdestruct` before reverting. This ensures that the gas is fully consumed before the revert occurs, preventing the gas griefing attack.