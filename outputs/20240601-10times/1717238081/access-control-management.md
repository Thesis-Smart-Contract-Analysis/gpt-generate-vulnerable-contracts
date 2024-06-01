```solidity
// Vulnerable smart contract with Access Control Management vulnerability

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

In the vulnerable smart contract `AccessControlVulnerability`, the `addAdmin` function allows the owner to add admins without proper access control. This means that anyone can become an admin by calling this function. Additionally, the `changeOwner` function also lacks proper access control, allowing anyone to change the owner of the contract.

### Remediation:

To fix the Access Control Management vulnerability in the smart contract, you can implement a modifier to restrict access to certain functions based on specific conditions. Here is the remediated version of the smart contract:

```solidity
// Remediated smart contract with proper Access Control Management

pragma solidity ^0.8.0;

contract AccessControlRemediation {
    address public owner;
    mapping(address => bool) public admins;

    constructor() {
        owner = msg.sender;
        admins[msg.sender] = true; // Owner is automatically an admin
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    modifier onlyAdmin() {
        require(admins[msg.sender], "Only admins can call this function");
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

In the remediated smart contract `AccessControlRemediation`, we have added modifiers `onlyOwner` and `onlyAdmin` to restrict access to functions based on the role of the caller. The `addAdmin` function can now only be called by the owner, ensuring that only the owner can add admins. The `changeOwner` function is also restricted to the owner only. Additionally, we have set the owner as an admin by default in the constructor.