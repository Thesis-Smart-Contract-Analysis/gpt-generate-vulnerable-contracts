### 1. **Use of `keccak256` with `block.blockhash` for Randomness**

**Severity:**
High

**Description:**
Using `keccak256` with `block.blockhash` for generating randomness is not secure as miners can manipulate the blockhash to their advantage. This can lead to a predictable outcome, allowing attackers to game the system.

**Locations:**

- In the constructor function:
  ```solidity
  answer = uint8(keccak256(block.blockhash(block.number - 1), now));
  ```

**Mitigation:**
To improve randomness, consider using a more secure source of randomness such as an oracle service or a verifiable random function (VRF). Avoid relying on `blockhash` for generating random numbers in smart contracts to prevent potential exploits.