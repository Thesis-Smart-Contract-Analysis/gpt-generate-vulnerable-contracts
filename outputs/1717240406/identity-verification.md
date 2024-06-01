Below is a vulnerable smart contract with Identity Verification vulnerability:

```solidity
pragma solidity ^0.8.0;

contract IdentityVerification {
    address public owner;
    mapping(address => bool) public verifiedUsers;

    constructor() {
        owner = msg.sender;
    }

    function verifyUser(address _user) public {
        require(msg.sender == owner, "Only owner can verify users");
        verifiedUsers[_user] = true;
    }

    function isUserVerified(address _user) public view returns (bool) {
        return verifiedUsers[_user];
    }
}
```

In the above smart contract, the `verifyUser` function allows the owner to mark a user as verified. However, the vulnerability lies in the fact that the verification process is solely based on the owner's address, which can be easily manipulated by an attacker.

An attacker can deploy a malicious contract with a fallback function that changes the owner's address of the `IdentityVerification` contract to their own address. This way, the attacker can then call the `verifyUser` function and mark any user as verified.

To remediate the Identity Verification vulnerability, you can implement a more secure verification process such as using a multi-signature scheme where multiple parties need to approve the verification of a user. This adds an extra layer of security and prevents a single point of failure.

Here is an updated version of the smart contract with a multi-signature verification process:

```solidity
pragma solidity ^0.8.0;

contract IdentityVerification {
    address public owner;
    mapping(address => bool) public verifiedUsers;
    mapping(address => bool) public verifiers;

    constructor() {
        owner = msg.sender;
        verifiers[msg.sender] = true;
    }

    function addVerifier(address _verifier) public {
        require(msg.sender == owner, "Only owner can add verifiers");
        verifiers[_verifier] = true;
    }

    function verifyUser(address _user) public {
        require(verifiers[msg.sender], "Only verifiers can verify users");
        verifiedUsers[_user] = true;
    }

    function isUserVerified(address _user) public view returns (bool) {
        return verifiedUsers[_user];
    }
}
```

In the updated version, the `addVerifier` function allows the owner to add verifiers who have the authority to verify users. This multi-signature approach ensures that multiple parties need to approve the verification process, making it more secure and less prone to manipulation by a single entity.