Below is a vulnerable smart contract that exhibits the Unexpected Balance vulnerability:

```solidity
pragma solidity ^0.8.0;

contract VulnerableContract {
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    function deposit() public payable {
        // Deposit ETH to the contract
    }
    
    function withdraw() public {
        require(msg.sender == owner, "Only the owner can withdraw");
        payable(msg.sender).transfer(address(this).balance);
    }
}
```

In the above smart contract, the `withdraw` function allows the owner to withdraw the entire balance of the contract. However, this function does not take into account the possibility of reentrancy attacks. An attacker can create a malicious contract that calls the `withdraw` function repeatedly before the balance is actually transferred, resulting in unexpected behavior.

### Remediation:

To mitigate the Unexpected Balance vulnerability, you can use the Check-Effect-Interaction pattern along with a mutex to prevent reentrancy attacks. Here is an updated version of the smart contract with the remediation:

```solidity
pragma solidity ^0.8.0;

contract SecureContract {
    address public owner;
    bool private _locked;
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }
    
    modifier lock {
        require(!_locked, "Reentrancy attack detected");
        _locked = true;
        _;
        _locked = false;
    }
    
    function deposit() public payable {
        // Deposit ETH to the contract
    }
    
    function withdraw() public onlyOwner lock {
        uint256 balance = address(this).balance;
        require(balance > 0, "No balance to withdraw");
        payable(owner).transfer(balance);
    }
}
```

In the remediated version:
1. The `onlyOwner` modifier ensures that only the owner can call the `withdraw` function.
2. The `lock` modifier prevents reentrancy attacks by setting a mutex that restricts multiple calls to the function before the current call completes.
3. The `withdraw` function now checks for a non-zero balance before transferring the funds to the owner.

By implementing these changes, the smart contract is more secure against reentrancy attacks and ensures that the balance is handled correctly during withdrawals.