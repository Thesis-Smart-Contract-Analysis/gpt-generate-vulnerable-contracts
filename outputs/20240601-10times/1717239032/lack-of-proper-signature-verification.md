Below is a vulnerable smart contract that lacks proper signature verification:

```solidity
pragma solidity ^0.8.0;

contract SignatureVerification {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address newOwner) public {
        require(msg.sender == owner, "Only the owner can transfer ownership");
        owner = newOwner;
    }

    function verifySignature(bytes32 message, uint8 v, bytes32 r, bytes32 s) public view returns (address) {
        address signer = ecrecover(message, v, r, s);
        return signer;
    }
}
```

In the `verifySignature` function, the contract attempts to verify a signature using the `ecrecover` function. However, it lacks proper validation of the recovered signer address. This can lead to unauthorized parties being able to call functions on behalf of the owner by providing a valid signature.

### Remediation:
To address the Lack of Proper Signature Verification vulnerability, you should implement additional checks to ensure that the recovered signer address matches the expected owner address before allowing any critical operations to be executed.

Here is an updated version of the smart contract with proper signature verification:

```solidity
pragma solidity ^0.8.0;

contract SignatureVerificationFixed {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address newOwner, bytes32 message, uint8 v, bytes32 r, bytes32 s) public {
        require(msg.sender == owner, "Only the owner can transfer ownership");
        
        address signer = ecrecover(message, v, r, s);
        require(signer == owner, "Invalid signature");
        
        owner = newOwner;
    }

    function verifySignature(bytes32 message, uint8 v, bytes32 r, bytes32 s) public view returns (address) {
        address signer = ecrecover(message, v, r, s);
        return signer;
    }
}
```

In the `transferOwnership` function, we added an additional check to ensure that the recovered signer address matches the current owner address before allowing the ownership transfer. This helps prevent unauthorized parties from transferring ownership using valid signatures.