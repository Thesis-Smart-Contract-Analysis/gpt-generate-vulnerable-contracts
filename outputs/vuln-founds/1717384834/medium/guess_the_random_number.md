### 1. **Vulnerability Type**

**Severity:**
Medium

**Description:**
The contract uses the `keccak256` function with `block.blockhash(block.number - 1)` and `now` to generate a random number for the answer. This method is susceptible to manipulation by miners in a block timestamp attack.

**Locations:**

- In the constructor function:
  ```solidity
  answer = uint8(keccak256(block.blockhash(block.number - 1), now));
  ```

**Mitigation:**
To mitigate this vulnerability, consider using a more secure source of randomness, such as an oracle service or a commit-reveal scheme. Avoid relying on block variables for generating random numbers in a secure context.