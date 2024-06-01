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

In the `verifySignature` function, the contract attempts to recover the address of the signer using the ECDSA signature provided. However, it lacks proper validation of the recovered address against the expected owner address. This can lead to unauthorized parties being able to call the `transferOwnership` function and take over the ownership of the contract.

### Remediation:
To address the Lack of Proper Signature Verification vulnerability, you should implement a proper signature verification process in the `verifySignature` function. Here is an updated version of the contract with a remediation:

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
        require(signer == owner, "Signature verification failed");
        return signer;
    }
}
```

In the remediated version, after recovering the address of the signer, the function now includes a `require` statement to verify that the recovered address matches the expected owner address. This ensures that only the rightful owner can successfully verify the signature and prevents unauthorized parties from taking over the ownership of the contract.