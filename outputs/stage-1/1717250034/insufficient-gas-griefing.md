Below is a vulnerable smart contract that exhibits the Insufficient Gas Griefing vulnerability:

```solidity
// Vulnerable Smart Contract with Insufficient Gas Griefing Vulnerability

pragma solidity ^0.8.0;

contract InsufficientGasGriefing {
    address public owner;
    uint public balance;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address _newOwner) public {
        require(msg.sender == owner, "Only the owner can transfer ownership");
        owner = _newOwner;
    }

    function withdrawBalance() public {
        require(msg.sender == owner, "Only the owner can withdraw balance");
        balance = address(this).balance;
        owner.transfer(balance);
    }

    function() external payable {
        // Revert the transaction to cause gas griefing
        revert("Gas griefing attack");
    }
}
```

In the above smart contract, the fallback function is designed to revert the transaction with a message "Gas griefing attack". This can be exploited by an attacker to perform a gas griefing attack, where they can send a small amount of Ether to the contract and trigger the fallback function repeatedly to consume the gas of the caller.

### Remediation:

To mitigate the Insufficient Gas Griefing vulnerability, you can implement a gas stipend mechanism in the fallback function. This mechanism limits the amount of gas that can be consumed by the fallback function, preventing gas griefing attacks.

Here is the remediated version of the smart contract:

```solidity
// Remediated Smart Contract with Gas Stipend Mechanism

pragma solidity ^0.8.0;

contract GasGriefingRemediation {
    address public owner;
    uint public balance;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address _newOwner) public {
        require(msg.sender == owner, "Only the owner can transfer ownership");
        owner = _newOwner;
    }

    function withdrawBalance() public {
        require(msg.sender == owner, "Only the owner can withdraw balance");
        balance = address(this).balance;
        owner.transfer(balance);
    }

    receive() external payable {
        // Implement gas stipend mechanism to limit gas usage
        require(msg.sender == owner, "Only the owner can send Ether");
        require(gasleft() > 2300, "Insufficient gas");
    }
}
```

In the remediated version, the `receive` function is used instead of the fallback function, and a gas stipend mechanism is implemented to check if the gas left is above a certain threshold (2300 gas in this case) before allowing the transaction to proceed. This helps prevent gas griefing attacks by limiting the gas consumption in the fallback function.