Below is a vulnerable smart contract with Access Control Management vulnerability:

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

    function changeOwner(address _newOwner) public {
        require(msg.sender == owner);
        owner = _newOwner;
    }
}
```

In the above smart contract, the `addAdmin` function allows the owner to add new admins to the `admins` mapping without proper access control. This means that anyone can call the `addAdmin` function and become an admin, potentially gaining unauthorized access to certain functionalities.

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

    function changeOwner(address _newOwner) public onlyOwner {
        owner = _newOwner;
    }
}
```

In the remediated version, the `onlyOwner` modifier is added to the `addAdmin` and `changeOwner` functions to ensure that only the owner can add new admins or change the owner address. This helps in properly managing access control and prevents unauthorized users from gaining admin privileges.