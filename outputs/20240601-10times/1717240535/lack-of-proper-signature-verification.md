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

    function verifySignature(bytes32 message, bytes memory signature) public view returns (address) {
        address signer = ECDSA.recover(message, signature);
        return signer;
    }
}
```

In the `verifySignature` function, the contract attempts to recover the address of the signer using the provided message and signature. However, it lacks proper validation of the recovered address against the expected owner address. This can lead to unauthorized parties being able to call the `transferOwnership` function and change the owner of the contract.

### Remediation:

To address the Lack of Proper Signature Verification vulnerability, you should implement a proper signature verification process in the `verifySignature` function. Here is an updated version of the smart contract with remediation:

```solidity
pragma solidity ^0.8.0;

contract SignatureVerification {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address newOwner, bytes32 message, bytes memory signature) public {
        address signer = ECDSA.recover(message, signature);
        require(signer == owner, "Signature verification failed");
        owner = newOwner;
    }

    function verifySignature(bytes32 message, bytes memory signature) public view returns (address) {
        address signer = ECDSA.recover(message, signature);
        return signer;
    }
}
```

In the remediated version, the `transferOwnership` function now includes signature verification before allowing the ownership transfer. The function verifies that the recovered signer address matches the current owner address before proceeding with the ownership transfer. This ensures that only the rightful owner can change the ownership of the contract.