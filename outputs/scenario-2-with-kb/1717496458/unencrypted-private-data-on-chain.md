# Smart Contract

```solidity
pragma solidity ^0.4.24;

contract UnencryptedPrivateData {
    // Private data stored on-chain
    uint private secretNumber = 42;
    string private secretString = "This is a secret";

    function revealSecret() public view returns (uint, string) {
        return (secretNumber, secretString); // line 7
    }
}
```

The vulnerability in the above smart contract lies in the fact that even though the state variables `secretNumber` and `secretString` are declared as `private`, they are still part of the blockchain's immutable and transparent ledger. This means that anyone with access to the blockchain can potentially view these values, despite the `private` keyword, which only restricts visibility at the contract level and not at the blockchain level.

# Remediations

1. **Avoid Storing Sensitive Data On-Chain**: The most secure way to handle sensitive data is not to store it on the blockchain. Consider storing such data off-chain and only keeping references or hashes on-chain if necessary.

2. **Encryption Before Storing**: If storing sensitive data on-chain is unavoidable, consider encrypting the data before it is stored. However, managing encryption keys securely within the context of a smart contract can be challenging and might require additional off-chain infrastructure.

3. **Use Hashing for Validation**: If the integrity of the data needs to be verified without revealing the actual data, consider storing a hash of the data instead of the data itself. This approach is useful for validation purposes without exposing the underlying sensitive data.

By implementing these remediations, the security of sensitive data in smart contracts can be significantly enhanced, protecting it from unauthorized access despite the public nature of blockchain data.