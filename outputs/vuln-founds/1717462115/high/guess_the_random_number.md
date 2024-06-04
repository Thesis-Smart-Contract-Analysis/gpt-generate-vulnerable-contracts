### 1. **Vulnerability Type**

**Severity:**
High

**Description:**
The vulnerability lies in the use of `block.blockhash(block.number - 1)` and `now` to generate randomness. This method is predictable and can be manipulated by miners to influence the outcome of the random number generation.

**Locations:**

- In the constructor function:
  ```solidity
  answer = uint8(keccak256(block.blockhash(block.number - 1), now));
  ```

**Mitigation:**
To mitigate this vulnerability, it is recommended to use a more secure and reliable source of randomness, such as Chainlink VRF (Verifiable Random Function) or an oracle service. By integrating a secure randomness solution, the contract can ensure that the generated numbers are not predictable or manipulatable by external actors.