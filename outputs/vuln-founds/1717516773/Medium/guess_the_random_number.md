### 1. **Use of `keccak256` for Random Number Generation**

**Severity:**
Medium

**Description:**
Using `keccak256` for generating random numbers can be predictable and manipulable by miners or attackers, leading to potential exploits in the contract.

**Locations:**

- In the constructor function:
  ```solidity
  answer = uint8(keccak256(block.blockhash(block.number - 1), now));
  ```

**Mitigation:**
Avoid using `keccak256` for generating random numbers as it can be manipulated. Consider using a more secure source of randomness, such as Chainlink VRF or Oraclize. If randomness is not critical, consider using a different approach that does not rely on on-chain randomness.