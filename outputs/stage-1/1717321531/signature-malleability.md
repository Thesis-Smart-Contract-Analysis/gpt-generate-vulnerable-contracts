# Smart contract

```solidity
pragma solidity ^0.4.24;

contract SignatureMalleability {
    
    function verifySignature(bytes32 hash, uint8 v, bytes32 r, bytes32 s) public pure returns (address) {
        address signer = ecrecover(hash, v, r, s);
        return signer;
    }
    
}
```

Description: The vulnerability in the above smart contract lies in the `verifySignature` function. The `ecrecover` function in Solidity is susceptible to signature malleability, which means that multiple valid signatures can exist for the same message. This can lead to unexpected behavior or security issues in the smart contract.

# Remediations

- Use a library like OpenZeppelin's ECDSA library to handle signature verification securely.
- Implement additional checks or validation mechanisms to ensure the uniqueness and integrity of signatures.