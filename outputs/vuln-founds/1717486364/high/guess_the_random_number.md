### 1. **Vulnerability Type**

**Severity:**
High

**Description:**
The vulnerability lies in the use of `block.blockhash(block.number - 1)` and `now` to generate the random number for the `answer` variable. This approach is susceptible to manipulation by miners or external attackers.

**Locations:**

- In the constructor function:
  ```solidity
  answer = uint8(keccak256(block.blockhash(block.number - 1), now));
  ```

**Mitigation:**
To mitigate this vulnerability, it is recommended to use a more secure source of randomness, such as Chainlink VRF (Verifiable Random Function) or an oracle service. Avoid relying on block-related data or timestamps for generating random numbers in smart contracts to prevent manipulation.