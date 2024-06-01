Below is a vulnerable smart contract with the Frozen Ether vulnerability:

```solidity
pragma solidity ^0.8.0;

contract FrozenEther {
    address public owner;
    bool public isFrozen;

    constructor() {
        owner = msg.sender;
        isFrozen = true;
    }

    function freeze() public {
        require(msg.sender == owner, "Only the owner can freeze");
        isFrozen = true;
    }

    function unfreeze() public {
        require(msg.sender == owner, "Only the owner can unfreeze");
        isFrozen = false;
    }

    function withdraw() public {
        require(!isFrozen, "Contract is frozen");
        payable(msg.sender).transfer(address(this).balance);
    }
}
```

In the `FrozenEther` contract above, the owner can freeze and unfreeze the contract using the `freeze` and `unfreeze` functions. When the contract is frozen, the `withdraw` function will not allow any withdrawals, effectively freezing the Ether held in the contract.

### Remediation:
To address the Frozen Ether vulnerability, you can implement a withdrawal pattern where users need to request a withdrawal instead of directly allowing withdrawals. Here is an updated version of the contract with the remediation:

```solidity
pragma solidity ^0.8.0;

contract FixedFrozenEther {
    address public owner;
    bool public isFrozen;
    mapping(address => uint256) public pendingWithdrawals;

    constructor() {
        owner = msg.sender;
        isFrozen = true;
    }

    function freeze() public {
        require(msg.sender == owner, "Only the owner can freeze");
        isFrozen = true;
    }

    function unfreeze() public {
        require(msg.sender == owner, "Only the owner can unfreeze");
        isFrozen = false;
    }

    function requestWithdrawal() public {
        require(!isFrozen, "Contract is frozen");
        pendingWithdrawals[msg.sender] += address(this).balance;
    }

    function withdraw() public {
        uint256 amount = pendingWithdrawals[msg.sender];
        require(amount > 0, "No pending withdrawals");
        pendingWithdrawals[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}
```

In the `FixedFrozenEther` contract, users can request a withdrawal using the `requestWithdrawal` function, which adds the withdrawal amount to their pending withdrawals. The `withdraw` function allows users to withdraw their pending balance, ensuring that the contract owner cannot freeze the Ether indefinitely.