### 1. **Use of `keccak256` for Random Number Generation**

**Severity:**
Informational

**Description:**
Using `keccak256` for generating random numbers can be predictable and manipulable by miners or attackers. It can lead to potential exploits in the contract.

**Locations:**

- In the constructor function:
  ```solidity
  answer = uint8(keccak256(block.blockhash(block.number - 1), now));
  ```

**Mitigation:**
To improve randomness, consider using an external oracle or Chainlink VRF (Verifiable Random Function) for secure random number generation. Avoid using block-related data for randomness as it can be manipulated.