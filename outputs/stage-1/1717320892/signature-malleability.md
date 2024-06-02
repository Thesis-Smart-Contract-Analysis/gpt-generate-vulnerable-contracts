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

The vulnerability lies in the `verifySignature` function where the `ecrecover` function is used to recover the address of the signer from the provided signature parameters. The issue here is that the `v` parameter can be manipulated to produce different valid signatures that correspond to the same message hash.

# Remediations

- Use a library like OpenZeppelin's ECDSA library to handle signature verification securely. This library provides functions that handle signature verification in a safe manner.
- Implement additional checks or validations to ensure that the recovered address is the expected signer and not vulnerable to signature malleability attacks.