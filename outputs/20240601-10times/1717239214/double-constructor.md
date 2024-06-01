Below is a vulnerable smart contract with Double Constructor vulnerability:

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

In the above smart contract, there are two constructors defined. This leads to the Double Constructor vulnerability where it is ambiguous which constructor will be called during deployment. This can lead to unexpected behavior and potential security risks.

### Remediation:

To remediate the Double Constructor vulnerability, you should only have one constructor in your smart contract. If you need to have different initialization logic based on different parameters, you can achieve this by using function overloading or conditional logic within a single constructor.

Here is the remediated version of the smart contract:

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

By having a single constructor with parameters that define the initialization logic, you can avoid the Double Constructor vulnerability and ensure clarity in the deployment process.