Below is a vulnerable smart contract with the Double Constructor vulnerability:

```solidity
pragma solidity ^0.8.0;

contract DoubleConstructor {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    constructor(address _newOwner) {
        owner = _newOwner;
    }

    function getOwner() public view returns (address) {
        return owner;
    }
}
```

In the above smart contract `DoubleConstructor`, there are two constructors defined. This is not allowed in Solidity and can lead to unexpected behavior. The last defined constructor will override the previous one, and the contract will use the last constructor defined during deployment.

### Remediation:
To remediate the Double Constructor vulnerability, you should only have one constructor in the smart contract. If you need to have different initialization logic based on different parameters, you can use function overloading within a single constructor or use conditional statements inside the constructor.

Here is the remediated version of the smart contract `DoubleConstructor`:

```solidity
pragma solidity ^0.8.0;

contract SingleConstructor {
    address public owner;

    constructor(address _newOwner) {
        owner = _newOwner;
    }

    function getOwner() public view returns (address) {
        return owner;
    }
}
```

In the remediated version, we have removed the extra constructor and combined the functionality into a single constructor that takes an address parameter to set the owner. This ensures that there is no ambiguity in constructor selection during deployment.