```solidity
// Smart Contract with Access Control Management Vulnerability

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

    function removeAdmin(address _admin) public {
        require(msg.sender == owner);
        admins[_admin] = false;
    }
}
```

### Vulnerability Description:
The smart contract `AccessControlVulnerability` has an access control management vulnerability where the owner can add or remove admins without proper access control checks. This means that anyone who is the owner can manipulate the list of admins without any restrictions.

### Remediation:
To fix the access control management vulnerability, you should implement proper access control checks in the functions that modify the list of admins. Here is an updated version of the smart contract with improved access control:

```solidity
// Smart Contract with Fixed Access Control Management

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

    function removeAdmin(address _admin) public onlyOwner {
        admins[_admin] = false;
    }
}
```

In the fixed version:
1. Added a `onlyOwner` modifier to restrict access to functions that modify the list of admins only to the owner.
2. Modified the `addAdmin` and `removeAdmin` functions to use the `onlyOwner` modifier to ensure that only the owner can add or remove admins.

By implementing these changes, the smart contract now enforces proper access control management, preventing unauthorized manipulation of the admin list.