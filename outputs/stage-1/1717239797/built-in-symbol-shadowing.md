Below is a smart contract that demonstrates the Built-in Symbol Shadowing vulnerability:

```solidity
pragma solidity ^0.8.0;

contract SymbolShadowing {
    address owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address newOwner) public {
        require(msg.sender == owner, "Only the owner can transfer ownership");
        address owner = newOwner; // Symbol shadowing vulnerability
        owner = newOwner;
    }

    function getOwner() public view returns (address) {
        return owner;
    }
}
```

In the `transferOwnership` function of the `SymbolShadowing` contract, there is a variable named `owner` declared inside the function that shadows the state variable `owner`. This can lead to unexpected behavior as the state variable `owner` is not updated when the local variable `owner` is assigned a new value.

### Remediation:
To fix the Built-in Symbol Shadowing vulnerability, you should avoid using the same variable names for local variables that are the same as state variables. Here is the remediated version of the `SymbolShadowing` contract:

```solidity
pragma solidity ^0.8.0;

contract SymbolShadowingFixed {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address newOwner) public {
        require(msg.sender == owner, "Only the owner can transfer ownership");
        owner = newOwner; // Update the state variable directly
    }

    function getOwner() public view returns (address) {
        return owner;
    }
}
```

In the remediated version, the local variable `owner` inside the `transferOwnership` function has been removed, and the state variable `owner` is directly updated with the new owner address. This ensures that there is no shadowing of variables and the state variable is correctly updated.