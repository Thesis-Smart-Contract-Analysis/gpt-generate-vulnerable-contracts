### 1. **Use of `keccak256` for Random Number Generation**

**Severity:**
Medium

**Description:**
Using `keccak256` for generating random numbers can be predictable and manipulable by miners or attackers. This can lead to potential exploits in the contract.

**Locations:**

- In the constructor function:
  ```solidity
  answer = uint8(keccak256(block.blockhash(block.number - 1), now));
  ```

**Mitigation:**
To improve randomness and security, consider using an external random number oracle or Chainlink VRF (Verifiable Random Function) to generate random numbers securely. This will prevent miners or attackers from predicting the outcome and manipulating the randomness.