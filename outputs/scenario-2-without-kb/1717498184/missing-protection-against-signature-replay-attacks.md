# Smart Contract with Vulnerability

Here is an example of a simple Ethereum smart contract written in Solidity that demonstrates the Missing Protection against Signature Replay Attacks vulnerability:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ReplayAttackVulnerable {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // Event to log successful transactions
    event AuthorizedAction(address indexed from, uint256 amount);

    // Function to execute an action if the signature is valid
    function executeAction(uint256 amount, bytes memory signature) public {
        require(recoverSigner(getMessageHash(amount), signature) == owner, "Invalid signature");
        // Vulnerable Line: The signature is not checked whether it has been used before.
        emit AuthorizedAction(msg.sender, amount);
    }

    // This function returns the hash of the message
    function getMessageHash(uint256 amount) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(amount));
    }

    // This function recovers the signer from the hash and the signature
    function recoverSigner(bytes32 hash, bytes memory signature) public pure returns (address) {
        bytes32 ethSignedHash = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", hash));
        (bytes32 r, bytes32 s, uint8 v) = splitSignature(signature);
        return ecrecover(ethSignedHash, v, r, s);
    }

    // Helper function to split a signature into its components
    function splitSignature(bytes memory sig)
        public
        pure
        returns (bytes32 r, bytes32 s, uint8 v)
    {
        require(sig.length == 65, "Invalid signature length");

        assembly {
            r := mload(add(sig, 32))
            s := mload(add(sig, 64))
            v := byte(0, mload(add(sig, 96)))
        }
    }
}
```

### Description of the Vulnerability in the Generated Smart Contract

The vulnerability in this contract lies in the `executeAction` function where it checks if the signature is valid but does not verify whether the signature has already been used. This allows an attacker to replay the same signature multiple times to authorize actions, potentially leading to unauthorized or unintended transactions.

# Remediations

- **Remediation 1: Use a nonce**
  - Implement a nonce mechanism where each action must include a unique nonce. The nonce is incremented after each action, ensuring that each signature can only be used once. This prevents the replay of signatures.

- **Remediation 2: Maintain a signature registry**
  - Keep a registry (mapping) of used signatures in the contract. Before executing an action, check if the signature has already been registered as used, and mark it as used after the action is executed. This ensures that each signature can only be used once.

Here is an example of how to implement the first remediation:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ReplayAttackProtected {
    address public owner;
    mapping(address => uint256) public nonces;

    constructor() {
        owner = msg.sender;
    }

    event AuthorizedAction(address indexed from, uint256 amount);

    function executeAction(uint256 amount, uint256 nonce, bytes memory signature) public {
        require(nonce == nonces[msg.sender], "Invalid nonce");
        require(recoverSigner(getMessageHash(amount, nonce), signature) == owner, "Invalid signature");
        nonces[msg.sender]++;
        emit AuthorizedAction(msg.sender, amount);
    }

    function getMessageHash(uint256 amount, uint256 nonce) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(amount, nonce));
    }

    function recoverSigner(bytes32 hash, bytes memory signature) public pure returns (address) {
        bytes32 ethSignedHash = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", hash));
        (bytes32 r, bytes32 s, uint8 v) = splitSignature(signature);
        return ecrecover(ethSignedHash, v, r, s);
    }

    function splitSignature(bytes memory sig)
        public
        pure
        returns (bytes32 r, bytes32 s, uint8 v)
    {
        require(sig.length == 65, "Invalid signature length");

        assembly {
            r := mload(add(sig, 32))
            s := mload(add(sig, 64))
            v := byte(0, mload(add(sig, 96)))
        }
    }
}
```

In this revised version, the `executeAction` function now requires a nonce that must match the expected nonce for the sender, effectively preventing replay attacks.