### 1. **Use of `keccak256` for Random Number Generation**

**Severity:**
High

**Description:**
Using `keccak256` for generating random numbers can be predictable and manipulable by miners or attackers. This can lead to the possibility of front-running attacks or unfair advantage in guessing the random number.

**Locations:**

- In the constructor function:
  ```solidity
  answer = uint8(keccak256(block.blockhash(block.number - 1), now));
  ```

**Mitigation:**
To improve randomness and security, consider using an external random number oracle or Chainlink VRF (Verifiable Random Function) to generate random numbers securely on-chain. This will prevent miners or attackers from predicting or manipulating the random number generation process.