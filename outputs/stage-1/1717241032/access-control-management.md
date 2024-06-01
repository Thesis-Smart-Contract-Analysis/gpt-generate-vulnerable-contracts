Below is a vulnerable smart contract with Access Control Management issue:

```solidity
pragma solidity ^0.8.0;

contract AccessControlVulnerability {
    address public owner;
    mapping(address => bool) public admins;

    constructor() {
        owner = msg.sender;
    }

    function addAdmin(address _admin) public {
        require(msg.sender == owner);
        admins[_admin] = true;
    }

    function isAdmin(address _admin) public view returns (bool) {
        return admins[_admin];
    }
}
```

In the above smart contract `AccessControlVulnerability`, the `addAdmin` function allows the owner to add admins to the `admins` mapping without any additional access control checks. This means that anyone who is the owner can add any address as an admin without any restrictions.

### Remediation:
To fix the Access Control Management vulnerability in the smart contract, you can implement a modifier to restrict the `addAdmin` function to only be callable by the owner. Here is the remediated version of the smart contract:

```solidity
pragma solidity ^0.8.0;

contract AccessControlFixed {
    address public owner;
    mapping(address => bool) public admins;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    function addAdmin(address _admin) public onlyOwner {
        admins[_admin] = true;
    }

    function isAdmin(address _admin) public view returns (bool) {
        return admins[_admin];
    }
}
```

In the remediated version, the `onlyOwner` modifier is added to the `addAdmin` function to ensure that only the owner can add admins. This helps in properly managing access control and prevents unauthorized users from adding admins to the smart contract.