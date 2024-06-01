Below is a vulnerable smart contract with Incorrect Inheritance Order vulnerability:

```solidity
pragma solidity ^0.8.0;

contract Ownable {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }
}

contract Pausable {
    bool public paused;

    constructor() {
        paused = false;
    }

    modifier whenNotPaused {
        require(!paused, "Contract is paused");
        _;
    }
}

// Incorrect Inheritance Order
contract MyContract is Pausable, Ownable {
    uint public data;

    constructor() {
        data = 0;
    }

    function setData(uint _data) public onlyOwner whenNotPaused {
        data = _data;
    }

    function pauseContract() public onlyOwner {
        paused = true;
    }

    function unpauseContract() public onlyOwner {
        paused = false;
    }
}
```

In the above smart contract, the order of inheritance is incorrect. The `MyContract` contract inherits from `Pausable` first and then from `Ownable`. This can lead to unexpected behavior as the modifier `onlyOwner` from `Ownable` is applied before the modifier `whenNotPaused` from `Pausable`. This means that the `onlyOwner` modifier will be checked before the `whenNotPaused` modifier, which may not be the intended behavior.

### Remediation:
To fix the Incorrect Inheritance Order vulnerability, you should ensure that the order of inheritance is correct. In this case, `MyContract` should inherit from `Ownable` first and then from `Pausable`.

Here is the remediated version of the smart contract:

```solidity
// Correct Inheritance Order
contract MyContractFixed is Ownable, Pausable {
    uint public data;

    constructor() {
        data = 0;
    }

    function setData(uint _data) public onlyOwner whenNotPaused {
        data = _data;
    }

    function pauseContract() public onlyOwner {
        paused = true;
    }

    function unpauseContract() public onlyOwner {
        paused = false;
    }
}
```

By ensuring the correct order of inheritance, you can prevent unexpected behavior and ensure that the modifiers are applied in the intended order.