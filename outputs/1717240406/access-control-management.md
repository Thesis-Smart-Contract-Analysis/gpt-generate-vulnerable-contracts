Below is a vulnerable smart contract with Access Control Management vulnerability:

```solidity
pragma solidity ^0.8.0;

contract AccessControlVulnerability {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address newOwner) public {
        require(msg.sender == owner);
        owner = newOwner;
    }
}
```

In the smart contract `AccessControlVulnerability` above, the `transferOwnership` function allows anyone to call it and change the `owner` of the contract without any additional access control checks. This can lead to unauthorized ownership changes and potential security risks.

### Remediation:

To address the Access Control Management vulnerability in the smart contract, you can implement a modifier to restrict the `transferOwnership` function to only be called by the current owner. Here is the remediated version of the smart contract:

```solidity
pragma solidity ^0.8.0;

contract AccessControlRemediation {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    function transferOwnership(address newOwner) public onlyOwner {
        owner = newOwner;
    }
}
```

In the remediated version, the `onlyOwner` modifier is added to the `transferOwnership` function to ensure that only the current owner can call this function. This helps to prevent unauthorized ownership changes and enhances the access control management of the smart contract.