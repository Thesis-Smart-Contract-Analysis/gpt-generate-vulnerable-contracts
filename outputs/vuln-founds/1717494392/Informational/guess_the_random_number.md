### 1. **Use of `keccak256` with `block.blockhash` for Randomness**

**Severity:**
Informational

**Description:**
Using `keccak256` with `block.blockhash` for generating randomness is not a secure method as it can be manipulated by miners. This can lead to a predictable outcome in the random number generation process.

**Locations:**

- In the constructor function:
  ```solidity
  answer = uint8(keccak256(block.blockhash(block.number - 1), now));
  ```

**Mitigation:**
To improve randomness, consider using a more secure source of randomness such as Chainlink VRF (Verifiable Random Function) or an oracle service. It's important to avoid using block-related data for generating random numbers in smart contracts.