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

Description of the vulnerability in the above smart contract:
The vulnerability in the `SignatureMalleability` contract lies in the `verifySignature` function. The `ecrecover` function in Solidity is susceptible to signature malleability, which means that multiple valid signatures can exist for the same message. An attacker can manipulate the `v`, `r`, and `s` parameters to create different valid signatures for the same message, leading to potential security risks.

# Remediations

- Use a library like OpenZeppelin's ECDSA library to handle signature verification securely.
- Implement additional checks or validation mechanisms to ensure the integrity and uniqueness of signatures.