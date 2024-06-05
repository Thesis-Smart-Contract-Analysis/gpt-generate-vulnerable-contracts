### 1. **Use of `keccak256` for Randomness**

**Severity:**
High

**Description:**
Using `keccak256` to generate randomness in a smart contract is not secure as miners can manipulate the blockhash to predict the outcome. This can lead to a front-running attack where miners can influence the result of the random number generation.

**Locations:**

- In the constructor function:
  ```solidity
  answer = uint8(keccak256(block.blockhash(block.number - 1), now));
  ```

**Mitigation:**
To improve randomness, consider using an external oracle or a verifiable random function (VRF) to generate random numbers securely. Avoid using block-related data for randomness in smart contracts.