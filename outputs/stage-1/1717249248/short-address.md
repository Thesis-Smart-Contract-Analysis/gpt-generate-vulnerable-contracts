```solidity
// Smart contract with Short Address Vulnerability

pragma solidity ^0.8.0;

contract ShortAddressVulnerability {
    
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    function transferOwnership(address _newOwner) public {
        require(msg.sender == owner);
        owner = _newOwner;
    }
    
}
```

In the smart contract above, the `transferOwnership` function allows the owner to transfer ownership to a new address. However, it is vulnerable to the Short Address Attack. In this attack, a malicious user can send a transaction with a short address (less than 20 bytes) to the `transferOwnership` function, causing the comparison `msg.sender == owner` to fail and allowing the attacker to take over ownership.

### Remediation for Short Address Vulnerability

To prevent the Short Address Attack, you can add a check to ensure that the length of the sender's address is exactly 20 bytes. Here is the remediated version of the smart contract:

```solidity
// Smart contract with Remediation for Short Address Vulnerability

pragma solidity ^0.8.0;

contract ShortAddressVulnerabilityFixed {
    
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    function transferOwnership(address _newOwner) public {
        require(msg.sender == owner);
        require(_newOwner.length == 20, "Invalid address length");
        owner = _newOwner;
    }
    
}
```

In the remediated version, the `transferOwnership` function now includes a check to ensure that the length of the `_newOwner` address is exactly 20 bytes. This check helps prevent the Short Address Attack by verifying that the address passed in is of the correct length.